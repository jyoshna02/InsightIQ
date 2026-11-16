
import pandas as pd

def load_dataset(file):
    df = pd.read_csv(file)
    return df


def profile_dataset(df):

    profile = {
        "total_rows": len(df),
        "total_columns": len(df.columns),
        "columns": list(df.columns),
        "data_types": {
            col: str(dtype)
            for col, dtype in df.dtypes.items()
        },
        "missing_values": {
            col: int(value)
            for col, value in df.isnull().sum().items()
        },
        "preview": df.head(5).fillna("").astype(str).to_dict(
            orient="records"
        )
    }

    return profile
