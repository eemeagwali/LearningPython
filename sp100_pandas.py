# sp100_analysis_pandas.py

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the dataset
df = pd.read_csv("sp100.csv")

# Add a P/E column
df["P/E"] = df["Price"] / df["EPS"]

# 1. Top 10 Companies by P/E Ratio
print("1. Top 10 Companies by P/E Ratio")
print(df.sort_values("P/E", ascending=False).head(10))

# 2. Sector-wise P/E Summary (mean, median, std)
print("\n2. Sector-wise P/E Summary")
print(df.groupby("Sector")["P/E"].agg(["mean", "median", "std", "count"]))

# 3. Number of Companies per Sector (Bar Chart)
print("\n3. Companies per Sector")
df["Sector"].value_counts().plot(kind="bar", title="Companies per Sector")
plt.ylabel("Count")
plt.tight_layout()
plt.show()

# 4. Sector-wise Average EPS and Price (Side-by-side Bars)
print("\n4. Sector-wise Avg Price and EPS")
sector_stats = df.groupby("Sector")[["Price", "EPS"]].mean().sort_values("Price")
sector_stats.plot(kind="barh", figsize=(10, 6), title="Sector-wise Avg Price & EPS")
plt.xlabel("Average Value")
plt.tight_layout()
plt.show()

# 5. Highlight Outliers (P/E > Q3 + 1.5×IQR)
print("\n5. Outliers based on P/E")
q1 = df["P/E"].quantile(0.25)
q3 = df["P/E"].quantile(0.75)
iqr = q3 - q1
upper_bound = q3 + 1.5 * iqr
outliers = df[df["P/E"] > upper_bound]
print(outliers[["Name", "P/E"]])

# 6. Correlation Between Price and EPS
print("\n6. Correlation Between Price and EPS")
correlation = df["Price"].corr(df["EPS"])
print(f"Correlation between Price and EPS: {correlation:.2f}")

# 7. Scatter Plot: EPS vs. Price Colored by Sector
print("\n7. Scatter Plot: EPS vs Price by Sector")
plt.figure(figsize=(10, 6))
sns.scatterplot(data=df, x="EPS", y="Price", hue="Sector", palette="Set2", s=100)
plt.title("EPS vs Price by Sector")
plt.grid(True)
plt.tight_layout()
plt.show()

# 8. Create a New Column: Growth Category (based on P/E)
print("\n8. Growth Category")
df["Growth"] = pd.cut(df["P/E"],
                  	bins=[0, 10, 20, 30, df["P/E"].max()],
                  	labels=["Undervalued", "Fairly Valued", "Growth", "Speculative"])
print(df[["Name", "P/E", "Growth"]].head(10))

# 9. Average P/E per Sector — Sorted Bar Plot
print("\n9. Average P/E by Sector")
df.groupby("Sector")["P/E"].mean().sort_values().plot(kind="barh", title="Avg P/E by Sector", color='teal')
plt.xlabel("Average P/E")
plt.tight_layout()
plt.show()

# 10. Boxplot of P/E Ratios by Sector
print("\n10. Boxplot of P/E Ratios by Sector")
plt.figure(figsize=(12, 6))
sns.boxplot(data=df, x="Sector", y="P/E")
plt.xticks(rotation=90)
plt.title("P/E Ratios by Sector")
plt.tight_layout()
plt.show()

# 11. Sector with Highest Total Market Value Proxy (Price × EPS)
print("\n11. Sector by Total Market Value Proxy (Price × EPS)")
df["MarketValueProxy"] = df["Price"] * df["EPS"]
sector_mv = df.groupby("Sector")["MarketValueProxy"].sum().sort_values(ascending=False)
print(sector_mv)

# 12. Save Enriched Dataset to New CSV
print("\n12. Saving enriched dataset to 'sp100_enriched.csv'")
df.to_csv("sp100_enriched.csv", index=False)


