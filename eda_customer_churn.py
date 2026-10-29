
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt


# 1. Generate customer churn dataset
def generate_synthetic_churn_data(n=1000, seed=42):
    rng = np.random.default_rng(seed)

    genders = rng.choice(["Male", "Female"], n)
    senior = rng.choice([0, 1], n, p=[0.84, 0.16])
    partner = rng.choice(["Yes", "No"], n)
    dependents = rng.choice(["Yes", "No"], n, p=[0.3, 0.7])
    tenure = rng.integers(0, 73, n).astype(float)

    contract = rng.choice(
        ["Month-to-month", "One year", "Two year"],
        n, p=[0.55, 0.24, 0.21]
    )
    internet = rng.choice(
        ["DSL", "Fiber optic", "No"],
        n, p=[0.35, 0.45, 0.2]
    )
    paperless = rng.choice(["Yes", "No"], n, p=[0.6, 0.4])
    payment = rng.choice([
        "Electronic check", "Mailed check",
        "Bank transfer", "Credit card"
    ], n)

    monthly = np.round(
        rng.normal(65, 30, n).clip(18, 120), 2
    )
    total = np.clip(
        np.round(monthly * tenure + rng.normal(0, 50, n), 2),
        0, None
    )

    churn_score = (
        (contract == "Month-to-month") * 0.35
        + (tenure < 12) * 0.30
        + (internet == "Fiber optic") * 0.15
        + (monthly > 80) * 0.15
        + rng.normal(0, 0.15, n)
    )
    churn = np.where(churn_score > 0.45, "Yes", "No")

    df = pd.DataFrame({
        "customerID": [f"CUST-{10000+i}" for i in range(n)],
        "gender": genders,
        "SeniorCitizen": senior,
        "Partner": partner,
        "Dependents": dependents,
        "tenure": tenure,
        "InternetService": internet,
        "Contract": contract,
        "PaperlessBilling": paperless,
        "PaymentMethod": payment,
        "MonthlyCharges": monthly,
        "TotalCharges": total,
        "Churn": churn
    })

    # Introduce missing values
    for col, frac in [
        ("TotalCharges", 0.03),
        ("tenure", 0.02),
        ("InternetService", 0.01)
    ]:
        idx = rng.choice(df.index, int(n * frac), replace=False)
        df.loc[idx, col] = np.nan

    # Inconsistent text
    idx = rng.choice(df.index, int(n * 0.08), replace=False)
    df.loc[idx, "Partner"] = df.loc[idx, "Partner"].str.lower()

    # Blank strings in numeric column
    idx = rng.choice(df.index, int(n * 0.01), replace=False)
    df["TotalCharges"] = df["TotalCharges"].astype(object)
    df.loc[idx, "TotalCharges"] = " "

    # Add duplicate rows
    duplicates = df.sample(n=15, random_state=seed)
    df = pd.concat([df, duplicates], ignore_index=True)

    return df


# 2. Explore raw data
def explore_raw_data(df):
    print("\nSTEP 1: INITIAL EXPLORATION")
    print("=" * 50)
    print("Dataset shape:", df.shape)
    print("\nData types:\n", df.dtypes)
    print("\nMissing values:\n", df.isnull().sum())
    print("\nDuplicate rows:", df.duplicated().sum())
    print("\nNumeric summary:\n",
          df.select_dtypes(include=np.number).describe())


# 3. Clean the data
def clean_data(df):
    clean = df.copy()

    clean["TotalCharges"] = pd.to_numeric(
        clean["TotalCharges"], errors="coerce"
    )

    text_cols = clean.select_dtypes(
        include=["object", "str"]
    ).columns.drop("customerID")

    for col in text_cols:
        clean[col] = clean[col].astype("string").str.strip()

    yes_no_cols = [
        "Partner", "Dependents", "PaperlessBilling", "Churn"
    ]

    for col in yes_no_cols:
        clean[col] = clean[col].str.lower().map({
            "yes": "Yes",
            "no": "No"
        })

    before = len(clean)
    clean = clean.drop_duplicates()
    removed = before - len(clean)

    clean["tenure"] = clean["tenure"].fillna(
        clean["tenure"].median()
    )
    clean["TotalCharges"] = clean["TotalCharges"].fillna(
        clean["MonthlyCharges"] * clean["tenure"]
    )
    clean["InternetService"] = clean["InternetService"].fillna("No")

    clean = clean.reset_index(drop=True)

    print("\nSTEP 2: DATA CLEANING SUMMARY")
    print("Duplicate rows removed:", removed)
    print("Rows before cleaning:", before)
    print("Rows after cleaning:", len(clean))
    print("Remaining missing values:", clean.isnull().sum().sum())

    return clean


# 4. Analyze churn patterns
def analyze_churn_patterns(df):
    print("\nSTEP 3: CHURN PATTERN ANALYSIS")
    print("=" * 50)

    rate = (df["Churn"] == "Yes").mean() * 100
    print(f"Overall churn rate: {rate:.1f}%")

    print("\nChurn rate by Contract:")
    print(
        df.groupby("Contract")["Churn"]
        .apply(lambda s: (s == "Yes").mean() * 100)
        .round(1).sort_values(ascending=False)
    )

    print("\nChurn rate by Internet Service:")
    print(
        df.groupby("InternetService")["Churn"]
        .apply(lambda s: (s == "Yes").mean() * 100)
        .round(1).sort_values(ascending=False)
    )

    print("\nAverage tenure by churn status:")
    print(df.groupby("Churn")["tenure"].mean().round(1))

    print("\nAverage monthly charges by churn status:")
    print(df.groupby("Churn")["MonthlyCharges"].mean().round(2))


# 5. Create and save four visualizations
def create_visualizations(df):
    # Chart 1: Overall churn distribution
    counts = df["Churn"].value_counts()
    plt.figure(figsize=(6, 4))
    plt.bar(counts.index, counts.values)
    plt.title("Overall Churn Distribution")
    plt.xlabel("Churn")
    plt.ylabel("Number of Customers")
    plt.tight_layout()
    plt.savefig("chart_churn_distribution.png", dpi=150)
    plt.close()

    # Chart 2: Churn rate by contract
    rates = df.groupby("Contract")["Churn"].apply(
        lambda s: (s == "Yes").mean() * 100
    )
    rates = rates.reindex(
        ["Month-to-month", "One year", "Two year"]
    )

    plt.figure(figsize=(7, 4))
    plt.bar(rates.index, rates.values)
    plt.title("Churn Rate by Contract Type")
    plt.ylabel("Churn Rate (%)")
    plt.tight_layout()
    plt.savefig("chart_churn_by_contract.png", dpi=150)
    plt.close()

    # Chart 3: Tenure distribution by churn
    plt.figure(figsize=(7, 4))
    for label in ["No", "Yes"]:
        subset = df.loc[df["Churn"] == label, "tenure"]
        plt.hist(subset, bins=20, alpha=0.6, label=label)

    plt.title("Tenure Distribution by Churn Status")
    plt.xlabel("Tenure (months)")
    plt.ylabel("Number of Customers")
    plt.legend()
    plt.tight_layout()
    plt.savefig("chart_tenure_by_churn.png", dpi=150)
    plt.close()

    # Chart 4: Correlation heatmap
    numeric = df[
        ["SeniorCitizen", "tenure", "MonthlyCharges", "TotalCharges"]
    ]
    corr = numeric.corr()

    fig, ax = plt.subplots(figsize=(7, 5))
    im = ax.imshow(corr, vmin=-1, vmax=1, cmap="RdYlGn")

    ax.set_xticks(range(len(corr.columns)))
    ax.set_yticks(range(len(corr.columns)))
    ax.set_xticklabels(corr.columns, rotation=45, ha="right")
    ax.set_yticklabels(corr.columns)

    for i in range(len(corr)):
        for j in range(len(corr)):
            ax.text(j, i, f"{corr.iloc[i, j]:.2f}",
                    ha="center", va="center")

    ax.set_title("Correlation Between Numeric Features")
    fig.colorbar(im, ax=ax)
    fig.tight_layout()
    fig.savefig("chart_correlation_heatmap.png", dpi=150)
    plt.close(fig)

    print("\nSTEP 4: VISUALIZATIONS SAVED")
    print("chart_churn_distribution.png")
    print("chart_churn_by_contract.png")
    print("chart_tenure_by_churn.png")
    print("chart_correlation_heatmap.png")


# 6. Main program
if __name__ == "__main__":
    raw_df = generate_synthetic_churn_data(n=1000)

    raw_df.to_csv("customer_churn_raw.csv", index=False)
    print("Raw dataset saved.")

    explore_raw_data(raw_df)

    clean_df = clean_data(raw_df)
    clean_df.to_csv("customer_churn_cleaned.csv", index=False)
    print("Cleaned dataset saved.")

    analyze_churn_patterns(clean_df)
    create_visualizations(clean_df)

    print("\nEDA complete!")
