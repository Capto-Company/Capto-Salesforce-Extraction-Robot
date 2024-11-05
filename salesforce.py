from simple_salesforce import Salesforce
import requests
import pandas as pd
from io import StringIO
import os
import glob
import os
import platform
import subprocess


def authenticate_salesforce(username, password, security_token):
    """
    Authenticates with Salesforce and returns the Salesforce instance.
    """
    try:
        print("Attempting to authenticate with Salesforce...")
        sf = Salesforce(username=username, password=password, security_token=security_token)
        print("Authentication successful.")
        return sf
    except Exception as e:
        print(f"Failed to authenticate with Salesforce: {e}")
        exit()

def clear_old_files(output_dir="output"):
    """
    Deletes old CSV files in the specified output directory.
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"Created directory: {output_dir}")
    else:
        old_files = glob.glob(os.path.join(output_dir, "*.csv"))
        for file_path in old_files:
            os.remove(file_path)
            print(f"Deleted old file: {file_path}")

def fetch_dataset_exports(sf):
    """
    Retrieves DatasetExport records and returns them.
    """
    soql_query = "SELECT Id, PublisherInfo FROM DatasetExport"
    try:
        print("Fetching DatasetExport records...")
        query_result = sf.query(soql_query)
        if query_result['totalSize'] > 0:
            return query_result['records']
        else:
            print("No DatasetExport records found.")
            return []
    except Exception as e:
        print(f"Error fetching DatasetExport records: {e}")
        return []

def download_dataset_parts(sf, dataset_export_id):
    """
    Downloads all parts for a given DatasetExport ID and combines them into a single CSV string.
    """
    print(f"Fetching parts for DatasetExport ID: {dataset_export_id}")
    soql_query = f"SELECT Id, PartNumber FROM DatasetExportPart WHERE DatasetExportId = '{dataset_export_id}' ORDER BY PartNumber"
    
    try:
        query_result = sf.query(soql_query)
        if query_result['totalSize'] > 0:
            all_parts = []
            for record in query_result['records']:
                part_id = record['Id']
                part_number = record['PartNumber']
                print(f"Downloading Part {part_number} with ID: {part_id}")
                part_url = f"https://{sf.sf_instance}/services/data/v56.0/sobjects/DatasetExportPart/{part_id}/DataFile"
                
                try:
                    response = requests.get(part_url, headers={'Authorization': f'Bearer {sf.session_id}'})
                    if response.status_code == 200:
                        all_parts.append(response.content.decode('utf-8'))
                    else:
                        print(f"Failed to download part {part_number}: {response.status_code}")
                except requests.exceptions.RequestException as e:
                    print(f"Error during download of part {part_number}: {e}")
                    continue
            combined_csv = ''.join(all_parts)
            return combined_csv
        else:
            print("No DatasetExportPart records found for this DatasetExport ID.")
            return None
    except Exception as e:
        print(f"Error fetching DatasetExportPart records: {e}")
        return None

def save_csv_in_chunks(df, base_filename, output_dir, chunk_size=100000):
    """
    Saves a DataFrame in multiple CSV files, each with a maximum of `chunk_size` rows.
    """
    num_chunks = len(df) // chunk_size + (1 if len(df) % chunk_size > 0 else 0)
    
    for i in range(num_chunks):
        chunk_df = df[i * chunk_size:(i + 1) * chunk_size]
        filename = f"{base_filename}_part_{i+1}.csv"
        filepath = os.path.join(output_dir, filename)
        chunk_df.to_csv(filepath, index=False)
        print(f"Saved {len(chunk_df)} rows to {filepath}")

def process_and_save_dataset(sf, dataset_export_id, publisher_info, output_dir="output"):
    """
    Processes each DatasetExport by downloading its parts, combining, and saving it in chunks.
    """
    combined_csv = download_dataset_parts(sf, dataset_export_id)
    
    if combined_csv:
        # Convert CSV string to DataFrame
        df = pd.read_csv(StringIO(combined_csv))
        print("Data preview:")
        print(df.head())

        # Shorter, more descriptive filename based on PublisherInfo and DatasetExport ID
        short_publisher = publisher_info.split(':')[1] if ':' in publisher_info else publisher_info
        base_filename = f"{short_publisher}_{dataset_export_id[:8]}"
        
        # Save DataFrame in chunks
        save_csv_in_chunks(df, base_filename, output_dir)

def open_output_folder(output_dir="output"):
    """
    Opens the output directory in the system's file explorer.
    """
    try:
        if platform.system() == "Windows":
            os.startfile(output_dir)
        elif platform.system() == "Darwin":  # macOS
            subprocess.Popen(["open", output_dir])
        elif platform.system() == "Linux":
            subprocess.Popen(["xdg-open", output_dir])
        print(f"Output folder '{output_dir}' opened successfully.")
    except Exception as e:
        print(f"Failed to open output folder: {e}")