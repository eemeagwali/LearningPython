"""
OMDb Analytics Script

This script fetches movie data from the OMDb API, builds a small dataset, cleans it,
and performs basic analytics suitable for an introductory data analytics lesson.

Outputs (created under ./outputs):
- omdb_movies.csv          → consolidated dataset
- correlation_heatmap.png  → numeric feature correlations
- rating_by_decade.png     → average IMDb rating by decade
- top_genres.png           → top genres by count and average rating
- votes_vs_rating.png      → IMDb votes vs rating scatter
- directors_avg_rating.png → top directors by average rating (min N films)

Usage examples (PowerShell on Windows):
  # Set your API key (get one from https://www.omdbapi.com/apikey.aspx)
  $env:OMDB_API_KEY = "YOUR_OMDB_API_KEY"

  # Run with defaults (terms: "the", pages per term: 10 → ~100 films)
  python "Python Programs/omdb_analysis.py"

  # Custom terms and pages
  python "Python Programs/omdb_analysis.py" --terms "the,love,man" --pages 5

Notes:
- The script caches per-title details in ./cache to minimize repeated API calls.
- Free OMDb keys have daily and rate limits; the script sleeps briefly between requests.
"""

from __future__ import annotations

import argparse
import json
import math
import os
import re
import time
from dataclasses import dataclass
from itertools import groupby
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Tuple

import numpy as np
import pandas as pd
import requests
import seaborn as sns
from matplotlib import pyplot as plt
from tqdm import tqdm

from Foodr import meals_df, stock_df, profit_by_eatery, stock_vs_orders, daily_revenue

OMDB_BASE_URL = "https://www.omdbapi.com/"


@dataclass
class FetchConfig:
    api_key: str
    search_terms: List[str]
    pages_per_term: int
    request_delay_seconds: float = 0.25
    cache_dir: Path = Path("Python Programs") / "cache"
    output_dir: Path = Path("Python Programs") / "outputs"


def get_api_key(cli_key: Optional[str]) -> str:
    """Resolve OMDb API key from CLI argument or environment variable.

    Raises a clear error with setup instructions if not provided.
    """
    if cli_key:
        return cli_key.strip()
    env_key = os.getenv("OMDB_API_KEY")
    if env_key:
        return env_key.strip()
    raise RuntimeError(
        "OMDb API key not found. Set the OMDB_API_KEY environment variable or pass "
        "--api-key. You can request a free key at https://www.omdbapi.com/apikey.aspx"
    )


def ensure_dirs(paths: Iterable[Path]) -> None:
    for p in paths:
        p.mkdir(parents=True, exist_ok=True)


def omdb_search(term: str, page: int, api_key: str) -> Dict:
    params = {
        "apikey": api_key,
        "s": term,
        "type": "movie",
        "page": page,
    }
    response = requests.get(OMDB_BASE_URL, params=params, timeout=20)
    response.raise_for_status()
    return response.json()


def omdb_fetch_details(imdb_id: str, api_key: str) -> Dict:
    params = {
        "apikey": api_key,
        "i": imdb_id,
        "plot": "short",
        "type": "movie",
    }
    response = requests.get(OMDB_BASE_URL, params=params, timeout=20)
    response.raise_for_status()
    return response.json()


def load_cache(cache_dir: Path) -> Dict[str, Dict]:
    cache_file = cache_dir / "omdb_movie_details.json"
    if cache_file.exists():
        try:
            return json.loads(cache_file.read_text(encoding="utf-8"))
        except Exception:
            return {}
    return {}


def save_cache(cache: Dict[str, Dict], cache_dir: Path) -> None:
    cache_file = cache_dir / "omdb_movie_details.json"
    cache_file.write_text(json.dumps(cache, indent=2), encoding="utf-8")


def collect_imdb_ids(config: FetchConfig) -> List[str]:
    """Collect IMDb IDs by searching for terms across pages.

    Returns a de-duplicated list of imdbIDs.
    """
    imdb_ids: List[str] = []
    for term in config.search_terms:
        for page in range(1, config.pages_per_term + 1):
            data = omdb_search(term=term, page=page, api_key=config.api_key)
            if data.get("Response") == "True" and "Search" in data:
                for item in data["Search"]:
                    imdb_id = item.get("imdbID")
                    if imdb_id:
                        imdb_ids.append(imdb_id)
            else:
                # No more pages for this term
                break
            time.sleep(config.request_delay_seconds)
    # Deduplicate preserving order
    seen = set()
    deduped: List[str] = []
    for _id in imdb_ids:
        if _id not in seen:
            seen.add(_id)
            deduped.append(_id)
    return deduped


def fetch_details_for_ids(imdb_ids: List[str], config: FetchConfig) -> List[Dict]:
    """Fetch detailed movie entries, using a simple on-disk cache to avoid refetching."""
    cache = load_cache(config.cache_dir)
    results: List[Dict] = []
    for imdb_id in tqdm(imdb_ids, desc="Fetching details"):
        if imdb_id in cache:
            results.append(cache[imdb_id])
            continue
        detail = omdb_fetch_details(imdb_id=imdb_id, api_key=config.api_key)
        if detail.get("Response") == "True":
            cache[imdb_id] = detail
            results.append(detail)
        # Even on errors, respect delay to be gentle to API
        time.sleep(config.request_delay_seconds)
    save_cache(cache, config.cache_dir)
    return results


def _to_int_safe(value: str) -> Optional[int]:
    try:
        if value is None or value == "N/A":
            return None
        return int(value)
    except Exception:
        return None


def _parse_year(year_field: str) -> Optional[int]:
    # OMDb Year can be "1999" or "1999–2003" or "1999-" etc.
    if not year_field or year_field == "N/A":
        return None
    match = re.match(r"(\d{4})", str(year_field))
    if match:
        return int(match.group(1))
    return None


def _parse_runtime(runtime_field: str) -> Optional[int]:
    # e.g., "121 min"
    if not runtime_field or runtime_field == "N/A":
        return None
    match = re.match(r"(\d+)\s*min", str(runtime_field))
    return int(match.group(1)) if match else None


def _parse_money(money_field: str) -> Optional[int]:
    # e.g., "$171,479,930"
    if not money_field or money_field == "N/A":
        return None
    numeric = re.sub(r"[^0-9]", "", str(money_field))
    return int(numeric) if numeric else None


def _parse_votes(votes_field: str) -> Optional[int]:
    if not votes_field or votes_field == "N/A":
        return None
    numeric = re.sub(r"[^0-9]", "", str(votes_field))
    return int(numeric) if numeric else None


def _parse_float_safe(value: str) -> Optional[float]:
    try:
        if value is None or value == "N/A":
            return None
        return float(value)
    except Exception:
        return None


def build_dataframe(raw_items: List[Dict]) -> pd.DataFrame:
    """Normalize raw OMDb movie detail objects into a DataFrame and clean types."""
    if not raw_items:
        return pd.DataFrame()
    df = pd.json_normalize(raw_items)

    # Select/rename columns of interest for teaching clarity
    column_map = {
        "imdbID": "imdb_id",
        "Title": "title",
        "Year": "year_raw",
        "Released": "released",
        "Runtime": "runtime_raw",
        "Genre": "genres",
        "Director": "director",
        "Writer": "writer",
        "Actors": "actors",
        "Language": "language",
        "Country": "country",
        "Awards": "awards",
        "imdbRating": "imdb_rating_raw",
        "imdbVotes": "imdb_votes_raw",
        "Metascore": "metascore_raw",
        "BoxOffice": "box_office_raw",
        "Production": "production",
        "Plot": "plot",
        "Rated": "rated",
    }
    df = df[[c for c in column_map.keys() if c in df.columns]].rename(columns=column_map)

    # Clean numeric fields
    df["year"] = df["year_raw"].apply(_parse_year)
    df["runtime_min"] = df["runtime_raw"].apply(_parse_runtime)
    df["imdb_rating"] = df["imdb_rating_raw"].apply(_parse_float_safe)
    df["imdb_votes"] = df["imdb_votes_raw"].apply(_parse_votes)
    df["metascore"] = df["metascore_raw"].apply(_to_int_safe)
    df["box_office_usd"] = df["box_office_raw"].apply(_parse_money)

    # Derived fields
    df["decade"] = df["year"].apply(lambda y: int(math.floor(y / 10.0) * 10) if isinstance(y, (int, float)) and not pd.isna(y) else None)

    # Standardize genres into list
    df["genres_list"] = df["genres"].fillna("").apply(lambda g: [s.strip() for s in str(g).split(",") if s.strip()])

    return df


def analyze_and_plot(df: pd.DataFrame, output_dir: Path) -> None:
    if df.empty:
        print("No data to analyze.")
        return

    ensure_dirs([output_dir])

    # Save consolidated CSV for students
    csv_path = output_dir / "omdb_movies.csv"
    df.to_csv(csv_path, index=False)
    print(f"Saved dataset → {csv_path}")

    # Set a seaborn theme for plots
    sns.set_theme(style="whitegrid")

    # 1) Correlation heatmap among numeric features
    numeric_cols = [
        "year",
        "runtime_min",
        "imdb_rating",
        "imdb_votes",
        "metascore",
        "box_office_usd",
    ]
    corr_df = df[numeric_cols].dropna(how="all").corr(numeric_only=True)
    plt.figure(figsize=(8, 6))
    sns.heatmap(corr_df, annot=True, cmap="crest", fmt=".2f", square=True)
    plt.title("Correlation Heatmap (Numeric Features)")
    plt.tight_layout()
    plt.savefig(output_dir / "correlation_heatmap.png", dpi=150)
    plt.close()

    # 2) Average IMDb rating by decade
    decade_df = (
        df.dropna(subset=["decade", "imdb_rating"])  # type: ignore[arg-type]
        .groupby("decade", as_index=False)["imdb_rating"]
        .mean()
        .sort_values("decade")
    )
    plt.figure(figsize=(9, 5))
    sns.lineplot(data=decade_df, x="decade", y="imdb_rating", marker="o")
    plt.title("Average IMDb Rating by Decade")
    plt.xlabel("Decade")
    plt.ylabel("Avg IMDb Rating")
    plt.tight_layout()
    plt.savefig(output_dir / "rating_by_decade.png", dpi=150)
    plt.close()

    # 3) Top genres by count and by average rating
    exploded = df.explode("genres_list")
    genre_counts = (
        exploded.dropna(subset=["genres_list"])  # type: ignore[arg-type]
        .groupby("genres_list")
        .size()
        .reset_index(name="count")
        .sort_values("count", ascending=False)
        .head(15)
    )
    plt.figure(figsize=(9, 6))
    sns.barplot(data=genre_counts, y="genres_list", x="count", palette="viridis")
    plt.title("Top Genres by Count")
    plt.xlabel("Count")
    plt.ylabel("Genre")
    plt.tight_layout()
    plt.savefig(output_dir / "top_genres.png", dpi=150)
    plt.close()

    genre_rating = (
        exploded.dropna(subset=["genres_list", "imdb_rating"])  # type: ignore[arg-type]
        .groupby("genres_list", as_index=False)["imdb_rating"]
        .mean()
        .sort_values("imdb_rating", ascending=False)
        .head(15)
    )
    plt.figure(figsize=(9, 6))
    sns.barplot(data=genre_rating, y="genres_list", x="imdb_rating", palette="magma")
    plt.title("Top Genres by Average IMDb Rating (Top 15)")
    plt.xlabel("Avg IMDb Rating")
    plt.ylabel("Genre")
    plt.tight_layout()
    plt.savefig(output_dir / "top_genres_by_rating.png", dpi=150)
    plt.close()

    # 4) IMDb votes vs rating (log votes), color by decade
    scatter_df = df.dropna(subset=["imdb_rating", "imdb_votes", "decade"]).copy()
    if not scatter_df.empty:
        scatter_df["log_votes"] = np.log10(scatter_df["imdb_votes"].clip(lower=1))
        plt.figure(figsize=(8.5, 6))
        sns.scatterplot(
            data=scatter_df,
            x="log_votes",
            y="imdb_rating",
            hue="decade",
            palette="Spectral",
            alpha=0.8,
        )
        plt.title("IMDb Votes (log10) vs Rating, colored by Decade")
        plt.xlabel("log10(ImdbVotes)")
        plt.ylabel("IMDb Rating")
        plt.tight_layout()
        plt.savefig(output_dir / "votes_vs_rating.png", dpi=150)
        plt.close()

    # 5) Directors by average rating (min 3 films)
    directors_df = df.dropna(subset=["director", "imdb_rating"]).copy()
    # Split multiple directors and explode
    directors_df["director_list"] = directors_df["director"].fillna("").apply(
        lambda d: [s.strip() for s in str(d).split(",") if s.strip()]
    )
    directors_exploded = directors_df.explode("director_list")
    agg = (
        directors_exploded.groupby("director_list", as_index=False)
        .agg(n_films=("imdb_id", "count"), avg_rating=("imdb_rating", "mean"))
        .query("n_films >= 3")
        .sort_values(["avg_rating", "n_films"], ascending=[False, False])
        .head(15)
    )
    if not agg.empty:
        plt.figure(figsize=(9, 6))
        sns.barplot(data=agg, y="director_list", x="avg_rating", hue="n_films", dodge=False, palette="coolwarm")
        plt.title("Top Directors by Avg IMDb Rating (min 3 films)")
        plt.xlabel("Avg IMDb Rating")
        plt.ylabel("Director")
        plt.legend(title="# Films", loc="lower right")
        plt.tight_layout()
        plt.savefig(output_dir / "directors_avg_rating.png", dpi=150)
        plt.close()

    # Simple textual summaries for teaching
    print("\nQuick descriptive stats (selected numeric columns):")
    print(df[["imdb_rating", "imdb_votes", "metascore", "runtime_min", "box_office_usd"]].describe())

    top_genres_text = genre_counts.head(10)
    print("\nTop 10 genres by count:")
    print(top_genres_text.to_string(index=False))

    print("\nSaved figures:")
    for fname in [
        "correlation_heatmap.png",
        "rating_by_decade.png",
        "top_genres.png",
        "top_genres_by_rating.png",
        "votes_vs_rating.png",
        "directors_avg_rating.png",
    ]:
        fpath = output_dir / fname
        if fpath.exists():
            print(f" - {fpath}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Fetch and analyze a small OMDb movie dataset.")
    parser.add_argument(
        "--terms",
        type=str,
        default="the",
        help="Comma-separated search terms (e.g., 'the,love,man'). Default: 'the'",
    )
    parser.add_argument(
        "--pages",
        type=int,
        default=10,
        help="Pages per term to fetch (10 results per page). Default: 10",
    )
    parser.add_argument(
        "--api-key",
        type=str,
        default=None,
        help="OMDb API key. If not provided, reads OMDB_API_KEY env var.",
    )
    parser.add_argument(
        "--delay",
        type=float,
        default=0.25,
        help="Delay between requests in seconds to respect rate limits. Default: 0.25",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    api_key = "32b714f6"
    terms = [t.strip() for t in args.terms.split(",") if t.strip()]
    config = FetchConfig(
        api_key=api_key,
        search_terms=terms,
        pages_per_term=max(1, int(args.pages)),
        request_delay_seconds=max(0.0, float(args.delay)),
    )

    ensure_dirs([config.cache_dir, config.output_dir])

    print(f"Searching OMDb for terms={terms} pages_per_term={config.pages_per_term} ...")
    imdb_ids = collect_imdb_ids(config)
    print(f"Found {len(imdb_ids)} unique IMDb IDs. Fetching details ...")

    raw_details = fetch_details_for_ids(imdb_ids, config)
    print(f"Fetched {len(raw_details)} detailed records. Building dataset ...")

    df = build_dataframe(raw_details)
    print(f"Dataset has {len(df)} rows and {len(df.columns)} columns after cleaning.")

    analyze_and_plot(df, config.output_dir)


if __name__ == "__main__":
    main()

#🐍 Foodr Analysis Tutorial with Pandas & NumPy
# ================================================
# ▶️ Required Libraries

import pandas as pd
import numpy as np
import psycopg2
from sqlalchemy import create_engine

# ▶️ Step 1: Connect to PostgreSQL (update with your credentials)

db_user = "postgres"
db_pass = "admin"
db_host = "localhost"
db_port = "5432"
db_name = "Foodr"
engine = create_engine(f"postgresql://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}")
print("✅ Connected to the database successfully!")

# ▶️ Step 2: Load tables into Pandas DataFrames

meals_df = pd.read_sql("SELECT * FROM meals", engine)
orders_df = pd.read_sql("SELECT * FROM orders", engine)
stock_df = pd.read_sql("SELECT * FROM stock", engine)
print("\nSample meals data:")
print(meals_df.head())
print("\nSample orders data:")
print(orders_df.head())
print("\nSample stock data:")
print(stock_df.head())

# ✅ Task 1: How many unique meals and eateries exist?

print("\n✅ Task 1: Unique Counts")
print("Unique meals:", meals_df["meal_id"].nunique())
print("Unique eateries:", meals_df["eatery"].nunique())

# ▶️ Step 3: Total revenue per meal

orders_df["order_revenue"] = orders_df["order_quantity"]*orders_df["meal_id"].map(
    meals_df.set_index("meal_id")["meal_price"]
)
revenue_per_meal =orders_df.groupby("meal_id")["order_revenue"].sum().reset_index()
revenue_per_meal = revenue_per_meal.merge(meals_df[["meal_id", "eatery"]], on="meal_id", how="left")
print("\n✅ Task 2: Top 5 revenue-generating meals:")
print(revenue_per_meal.sort_values(by="order_revenue", ascending=False).head())

# ▶️ Step 4: Profit per meal

meals_df["profit_margin"] = meals_df["meal_price"] - meals_df["meal_cost"]
orders_df["meal_cost"] = orders_df["meal_id"].map(meals_df.set_index("meal_id")["meal_cost"])
orders_df["meal_price"] =orders_df["meal_id"].map(meals_df.set_index("meal_id")["meal_price"])
orders_df["total_cost"] = orders_df["order_quantity"] * orders_df["meal_cost"]
orders_df["total_price"] = orders_df["order_quantity"] * orders_df["meal_price"]
orders_df["profit"] = orders_df["total_price"] - orders_df["total_cost"]
profit_by_eatery = orders_df.merge(meals_df[["meal_id", "eatery"]], on="meal_id", how="left") \
    \
    .groupby("eatery")["profit"].sum().sort_values(ascending=False).reset_index()
print("\n✅ Task 3: Total profit by eatery:")
print(profit_by_eatery)

# ▶️ Step 5: Analyze stock levels vs orders

stocked = stock_df.groupby("meal_id")["stocked_quantity"].sum()
ordered = orders_df.groupby("meal_id")["order_quantity"].sum()
stock_vs_orders = pd.DataFrame({
    "stocked": stocked,
    "ordered": ordered
}).fillna(0)
stock_vs_orders["leftover"] = stock_vs_orders["stocked"]-stock_vs_orders["ordered"]
print("\n✅ Task 4: Meals with negative leftover stock(oversold):")
print(stock_vs_orders[stock_vs_orders["leftover"]<0])

# ▶️ Step 6: Daily revenue trend using NumPy
daily_revenue = orders_df.groupby("order_date")["total_price"].sum().reset_index()
daily_revenue["7_day_avg"] = daily_revenue["total_price"].rolling(window=7).mean()
print("\n✅ Task 5: Revenue trend (last 10 days:")
print(daily_revenue.tail(10))
print("\n ✅ You’ve completed the Foodr Data Analysis Exercise!")