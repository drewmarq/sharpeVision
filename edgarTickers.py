import os
import json
import pandas as pd
import requests
import zipfile
import io

#downloads all CIKs with active stock tickers into a flat .csv file from SEC EDGAR's bulk .zip of .json files

# Define the URL for the ZIP file
zip_url = "https://www.sec.gov/Archives/edgar/daily-index/bulkdata/submissions.zip"

# Define headers with a User-Agent
headers = {
    'User-Agent': 'Meow - parker@protonmail.com'
}

# Initialize an empty DataFrame
data = pd.DataFrame(columns=["CIK", "Tickers", "Active_Ticker", "Filename", "SEC_EDGAR_CompanyFacts_URL"])

# Download the ZIP file
print("Downloading ZIP file...")
response = requests.get(zip_url, headers=headers)
response.raise_for_status()

# Extract the ZIP file in memory
with zipfile.ZipFile(io.BytesIO(response.content)) as z:
    file_list = [f for f in z.namelist() if f.endswith(".json") and "-submissions-" not in f]
    total_files = len(file_list)
    processed_files = 0

    # Iterate through the JSON files in the ZIP
    for filename in file_list:
        try:
            # Read the JSON file
            with z.open(filename) as file:
                data_content = json.load(file)

            # Check if 'tickers' exists in the JSON data
            if "tickers" in data_content:
                tickers = data_content["tickers"]

                # If tickers is a list, join it with commas
                if isinstance(tickers, list):
                    tickers = ", ".join(tickers)

                # Skip rows with empty tickers
                if not tickers.strip():
                    continue

                # Get the CIK and ensure proper padding
                raw_cik = str(data_content.get("cik", ""))
                print(f"Original CIK: {raw_cik}")  # Debug print
                
                # Force string conversion and pad
                padded_cik = str(raw_cik).zfill(10)
                print(f"Padded CIK: {padded_cik}")  # Debug print

                # Determine the active ticker
                active_ticker = tickers.split(",")[0].strip()

                # Construct the SEC EDGAR CompanyFacts URL with explicit padding
                company_facts_url = f"https://data.sec.gov/api/xbrl/companyfacts/CIK{padded_cik}.json"
                print(f"Generated URL: {company_facts_url}")  # Debug print

                # Store row data with explicitly padded CIK
                row_data = [[padded_cik, tickers, active_ticker, filename, company_facts_url]]
                
                # Check for duplicates before adding to the DataFrame
                if not ((data["Tickers"] == tickers) & (data["Filename"] == filename)).any():
                    data = pd.concat([data, pd.DataFrame(row_data, 
                                    columns=["CIK", "Tickers", "Active_Ticker", "Filename", "SEC_EDGAR_CompanyFacts_URL"])], 
                                    ignore_index=True)

        except Exception as e:
            print(f"Error processing file {filename}: {e}")

        # Update progress
        processed_files += 1
        if processed_files % 1000 == 0:  # Only print every 1000 files to reduce output
            print(f"Processed {processed_files}/{total_files} files...")

# Output the DataFrame to a CSV file
data.to_csv("tickers_output.csv", index=False)

# Print some sample rows to verify padding
print("\nSample of processed data:")
print(data.head())