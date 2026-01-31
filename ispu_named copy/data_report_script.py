import pandas as pd
import numpy as np
from pathlib import Path

# =====================
# CONFIG
# =====================
CSV_PATH = Path.cwd() / "ispu_all_years.csv"
NA_VALUES = ["---", "--", "", " ", "NA", "N/A"]

# =====================
# LOAD DATA
# =====================
df = pd.read_csv(CSV_PATH, na_values=NA_VALUES)

print("="*80)
print("DATASET OVERVIEW")
print("="*80)

print(f"Total rows    : {len(df):,}")
print(f"Total columns : {len(df.columns)}")
print("\nColumns:")
print(df.columns.tolist())

# =====================
# BASIC INFO
# =====================
print("\n" + "="*80)
print("BASIC INFO")
print("="*80)
print(df.info())

# =====================
# PER-COLUMN REPORT
# =====================
print("\n" + "="*80)
print("PER-COLUMN DATA QUALITY REPORT")
print("="*80)

report = []

for col in df.columns:
    total = len(df)
    null_count = df[col].isna().sum()
    unique_count = df[col].nunique(dropna=True)

    sample_values = (
        df[col]
        .dropna()
        .astype(str)
        .unique()[:5]
    )

    report.append({
        "column": col,
        "dtype": str(df[col].dtype),
        "null_count": null_count,
        "null_pct": round(null_count / total * 100, 2),
        "unique_values": unique_count,
        "sample_values": ", ".join(sample_values)
    })

report_df = pd.DataFrame(report)
print(report_df.sort_values("null_pct", ascending=False))

# =====================
# SPECIAL CHECKS
# =====================

print("\n" + "="*80)
print("SPECIAL ISPU CHECKS")
print("="*80)

# --- Check tanggal
if "tanggal" in df.columns:
    print("\n[TANGGAL CHECK]")
    parsed_date = pd.to_datetime(df["tanggal"], errors="coerce")
    invalid_date = parsed_date.isna().sum()

    print(f"Invalid tanggal rows : {invalid_date}")
    print(f"Min tanggal          : {parsed_date.min()}")
    print(f"Max tanggal          : {parsed_date.max()}")

# --- Check tahun coverage
if "period_data" in df.columns:
    print("\n[PERIOD DATA CHECK]")
    print("Unique years:", sorted(df["period_data"].astype(str).str[:4].unique()))

# --- Check kategori ISPU
if "categori" in df.columns:
    print("\n[CATEGORY DISTRIBUTION]")
    print(df["categori"].value_counts(dropna=False))

# --- Check critical pollutant
if "critical" in df.columns:
    print("\n[CRITICAL POLLUTANT DISTRIBUTION]")
    print(df["critical"].value_counts(dropna=False))

# --- Check stasiun
if "stasiun" in df.columns:
    print("\n[STASIUN DISTRIBUTION]")
    print(df["stasiun"].value_counts().head(10))

# =====================
# ID VALIDATION
# =====================
if "id" in df.columns:
    print("\n" + "="*80)
    print("ID VALIDATION")
    print("="*80)

    duplicate_ids = df["id"].duplicated().sum()
    null_ids = df["id"].isna().sum()

    print(f"Duplicate ID count : {duplicate_ids}")
    print(f"Null ID count      : {null_ids}")

    if duplicate_ids > 0:
        print("\nSample duplicated IDs:")
        print(df[df["id"].duplicated(keep=False)]["id"].head())

# =====================
# NUMERIC SANITY CHECK
# =====================
print("\n" + "="*80)
print("NUMERIC COLUMN SANITY CHECK")
print("="*80)

numeric_cols = df.select_dtypes(include=[np.number]).columns

for col in numeric_cols:
    print(f"\n[{col}]")
    print(df[col].describe())


