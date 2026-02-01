import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns



# =========================
# DISPLAY HELPER
# =========================
def display_styled(df):
    """
    Menampilkan dataframe dengan:
    - header & index rata kiri
    - nilai numerik rata kanan
    """
    sty = df.style.set_table_styles([
        {'selector': 'th.row_heading, th.col_heading',
         'props': [('text-align', 'left')]},
        {'selector': 'td',
         'props': [('text-align', 'right')]},
    ])
    display(sty)


# =========================
# SCHEMA CHECK
# =========================
def cek_schema(df):
    print("📌 Columns:")
    schema_df = pd.DataFrame({
        "column": df.columns,
        "dtype": df.dtypes.values
    })
    display_styled(schema_df)


# =========================
# NULL CHECK
# =========================
def cek_data_null(df):
    nulls = df.isna().sum()
    nulls = nulls[nulls > 0]

    if nulls.empty:
        print("✅ Tidak ada data null")
    else:
        print("⚠️ Kolom dengan data null:")
        display_styled(nulls.to_frame("jumlah_null"))


# =========================
# DUPLICATE CHECK
# =========================
def cek_duplikat(df, unique=None):
    """
    unique: str atau list kolom unik
            contoh: "tanggal" atau ["tanggal", "lokasi"]
    """
    if unique is None:
        print("ℹ️ Kolom unik tidak ditentukan, skip cek duplikat")
        return

    subset = [unique] if isinstance(unique, str) else list(unique)
    dup = df[df.duplicated(subset=subset, keep=False)]

    if dup.empty:
        print("✅ Tidak ada data duplikat")
    else:
        print(
            f"⚠️ Ditemukan {len(dup)} baris duplikat "
            f"({dup[subset].drop_duplicates().shape[0]} key)"
        )
        display_styled(dup.sort_values(subset))


# =========================
# BASIC STATISTICS
# =========================
def calculations(df):
    numeric_df = df.select_dtypes(include="number")

    if numeric_df.empty:
        print("⚠️ Tidak ada kolom numerik")
        return

    stats = numeric_df.describe().T
    display_styled(stats)


# =========================
# VISUALIZATION
# =========================
def visualization(df):
    numeric_df = df.select_dtypes(include="number")

    if numeric_df.empty:
        print("⚠️ Tidak ada kolom numerik untuk visualisasi")
        return

    # Boxplot
    numeric_df.plot(kind="box", figsize=(12, 5))
    plt.title("Boxplot Numerical Features")
    plt.show()

    # Heatmap korelasi
    plt.figure(figsize=(8, 6))
    sns.heatmap(numeric_df.corr(), annot=True, cmap="coolwarm")
    plt.title("Correlation Heatmap")
    plt.show()


# =========================
# COLUMN VALUE INSPECTOR
# =========================
# =========================
# COLUMN VALUE INSPECTOR
# =========================
def cek_value_data_column(
    df,
    exception=None,
    max_unique=None,
    return_df=True
):
    """
    Menampilkan unique values per kolom dalam format WIDE
    (kolom = nama kolom, baris = unique values)

    Parameters
    ----------
    df : pandas.DataFrame
    exception : list | set | str | None
        Kolom yang ingin di-skip
    max_unique : int | None
        Batas maksimum unique value per kolom
    return_df : bool
        Jika True, return DataFrame hasil
    """

    # normalisasi exception
    if exception is None:
        exception = set()
    elif isinstance(exception, str):
        exception = {exception}
    else:
        exception = set(exception)

    data = {}
    max_len = 0

    for col in df.columns:
        if col in exception:
            continue

        uniques = df[col].dropna().unique().tolist()

        if max_unique is not None:
            uniques = uniques[:max_unique]

        data[col] = uniques
        max_len = max(max_len, len(uniques))

    # samakan panjang list (biar bisa jadi DataFrame)
    for col, values in data.items():
        if len(values) < max_len:
            data[col] = values + [None] * (max_len - len(values))

    result_df = pd.DataFrame(data)

    print("📋 UNIQUE VALUE REPORT (WIDE FORMAT)")
    print(f"Total columns : {result_df.shape[1]}")
    print(f"Max rows      : {result_df.shape[0]}")

    display(result_df)

    if return_df:
        return result_df







# =========================
# MAIN EVALUATOR
# =========================
def evaluate_dataset(df, name=None, unique=None):
    print(f"\n================ {name or 'DATASET'} ================\n")

    display(df.head())
    cek_schema(df)
    cek_data_null(df)
    cek_duplikat(df, unique)
    calculations(df)
    visualization(df)


# =========================
# COLUMN NAME EXTRACTOR
# =========================
def extract_column_schema(dfs):
    """
    dfs: dict {nama_dataset: DataFrame}

    return:
        dict {
            dataset_name: {
                "columns": [...],
                "n_columns": int
            }
        }
    """
    schema_dict = {}

    for name, df in dfs.items():
        schema_dict[name] = {
            "columns": list(df.columns),
            "n_columns": len(df.columns)
        }

    return schema_dict




def find_internal_duplicate_columns(schema_dict):
    """
    Mendeteksi kolom duplikat dalam dataset yang sama
    (berdasarkan schema hasil extract_column_schema)
    """
    duplicates = {}

    for name, info in schema_dict.items():
        cols = info["columns"]  # ⬅️ ambil list kolomnya

        dup = [c for c in set(cols) if cols.count(c) > 1]
        if dup:
            duplicates[name] = dup

    return duplicates

def count_rows_per_dataset(dfs):
    """
    dfs: dict {nama_dataset: DataFrame}

    return:
        dict {
            nama_dataset: jumlah_row,
            "__total__": total_row
        }
    """
    summary = {}
    total_rows = 0

    for name, df in dfs.items():
        n_rows = len(df)
        summary[name] = n_rows
        total_rows += n_rows

    summary["__total__"] = total_rows
    return summary
    


def extract_single_schema(df):
    """
    Extract schema untuk satu DataFrame
    """
    return {
        "columns": list(df.columns),
        "n_columns": len(df.columns)
    }

