import os
from pathlib import Path
import pandas as pd
from azure.storage.blob import BlobServiceClient, ContentSettings

def ensure_data_dir():
    Path("data").mkdir(parents=True, exist_ok=True)

def upload_blob(account_name, account_key, container_name, source_file_path, dest_blob_name):
    try:
        conn_str = f"DefaultEndpointsProtocol=https;AccountName={account_name};AccountKey={account_key};EndpointSuffix=core.windows.net"
        blob_service_client = BlobServiceClient.from_connection_string(conn_str)
        container_client = blob_service_client.get_container_client(container_name)
        # create container if not exists (no harm if it exists)
        try:
            container_client.create_container()
            print(f"Created container: {container_name}")
        except Exception:
            pass

        with open(source_file_path, "rb") as data:
            content_settings = ContentSettings(content_type="text/csv")
            container_client.upload_blob(name=dest_blob_name, data=data, overwrite=True, content_settings=content_settings)
        print(f"Uploaded {source_file_path} to blob {container_name}/{dest_blob_name}")
    except Exception as e:
        print(f"ERROR uploading {source_file_path} to blob storage: {e}")
        raise

def process_sales_data():
    ensure_data_dir()

    src_path = Path("data") / "sales_data.csv"
    if not src_path.exists():
        raise FileNotFoundError(f"Input file not found: {src_path}. Place your sales_data.csv in the data/ folder.")

    # Read original sales data
    df = pd.read_csv(src_path)

    # Save unchanged raw copy
    raw_copy = Path("data") / "raw_sales_data.csv"
    df.to_csv(raw_copy, index=False)
    print(f"Saved raw copy to {raw_copy}")

    # Step 2: Drop duplicates based on order_id (keep first)
    if "order_id" not in df.columns:
        raise KeyError("Required column 'order_id' not found in input CSV.")
    before = len(df)
    df = df.drop_duplicates(subset=["order_id"], keep="first")
    after = len(df)
    print(f"Dropped {before - after} duplicate rows based on order_id.")

    # Step 3: Handle missing values
    # Replace missing region with "Unknown"
    if "region" in df.columns:
        df["region"] = df["region"].fillna("Unknown")
    else:
        # If region missing completely, create column
        df["region"] = "Unknown"

    # Replace missing revenue with 0
    if "revenue" in df.columns:
        # coerce to numeric (remove commas if present)
        df["revenue"] = pd.to_numeric(df["revenue"].astype(str).str.replace(",", ""), errors="coerce").fillna(0)
    else:
        df["revenue"] = 0

    # Ensure cost column exists and numeric
    if "cost" in df.columns:
        df["cost"] = pd.to_numeric(df["cost"].astype(str).str.replace(",", ""), errors="coerce").fillna(0)
    else:
        df["cost"] = 0

    # Step 4: Add calculated column profit_margin = (revenue - cost) / revenue
    # Avoid division by zero: if revenue == 0 set profit_margin = 0
    df["profit_margin"] = 0.0
    revenue_nonzero = df["revenue"] != 0
    df.loc[revenue_nonzero, "profit_margin"] = (df.loc[revenue_nonzero, "revenue"] - df.loc[revenue_nonzero, "cost"]) / df.loc[revenue_nonzero, "revenue"]

    # Step 5: Categorize customers into segments based on revenue
    # Platinum: revenue > 100000
    # Gold: 50000 < revenue <= 100000
    # Else: Standard
    def segment_by_revenue(r):
        try:
            r = float(r)
        except Exception:
            return "Standard"
        if r > 100000:
            return "Platinum"
        elif 50000 < r <= 100000:
            return "Gold"
        else:
            return "Standard"

    df["customer_segment"] = df["revenue"].apply(segment_by_revenue)

    # Normalize column names: lowercase and underscores
    df.columns = [str(c).strip().lower().replace(" ", "_") for c in df.columns]

    # Step 6: Save processed file
    processed_path = Path("data") / "processed_sales_data.csv"
    df.to_csv(processed_path, index=False)
    print(f"Saved processed data to {processed_path} (rows={len(df)})")

    return str(raw_copy), str(processed_path)

def main():
    raw_file, processed_file = process_sales_data()

    # Upload both files to Azure Blob Storage if environment variables are set
    account_name = os.environ.get("AZURE_STORAGE_ACCOUNT_NAME")
    account_key = os.environ.get("AZURE_STORAGE_ACCOUNT_KEY")
    container_name = os.environ.get("AZURE_CONTAINER_NAME")

    if not (account_name and account_key and container_name):
        print("Azure storage environment variables not fully set. Skipping upload to Blob Storage.")
        print("Set AZURE_STORAGE_ACCOUNT_NAME, AZURE_STORAGE_ACCOUNT_KEY, AZURE_CONTAINER_NAME to enable upload.")
        return

    # Upload raw and processed
    upload_blob(account_name, account_key, container_name, raw_file, Path(raw_file).name)
    upload_blob(account_name, account_key, container_name, processed_file, Path(processed_file).name)

if __name__ == "__main__":
    main()
