
# Salesforce Data Extraction Automation

This project provides an automated solution for extracting datasets from Salesforce using Python and Robot Framework.
It authenticates with Salesforce, retrieves available datasets, and processes them into manageable CSV files.

## Prerequisites

Ensure the following are installed on your system:

- **Python 3.x**: [Download Python](https://www.python.org/downloads/)
- **Robot Framework**: Install via pip:

  ```bash
  pip install robotframework
  ```

- **Simple Salesforce**: Install via pip:

  ```bash
  pip install simple-salesforce
  ```

- **Pandas**: Install via pip:

  ```bash
  pip install pandas
  ```

- **Requests**: Install via pip:

  ```bash
  pip install requests
  ```

## Project Structure

The project consists of the following files:

- `salesforce.py`: Contains Python functions for authenticating with Salesforce, fetching datasets, and processing them.
- `extract_salesforce_data.robot`: Robot Framework test suite that utilizes functions from `salesforce.py` to automate the data extraction process.

## Setup

1. **Salesforce Credentials**: Update the `*** Variables ***` section in `extract_salesforce_data.robot` with your Salesforce credentials:

   ```robot
   *** Variables ***
   ${username}          your_salesforce_username
   ${password}          your_salesforce_password
   ${security_token}    your_salesforce_security_token
   ```

2. **Output Directory**: Ensure an `exported_datasets` directory exists in the project root. This is where the extracted CSV files will be saved.

## Execution

To run the automation:

1. Open a terminal and navigate to the project directory.
2. Execute the Robot Framework test suite:

   ```bash
   robot extract_salesforce_data.robot
   ```

Upon completion, the `exported_datasets` directory will contain CSV files representing the extracted datasets.

## Functionality Overview

The automation performs the following steps:

1. **Authentication**: Connects to Salesforce using provided credentials.
2. **Clear Old Files**: Deletes existing CSV files in the `exported_datasets` directory to prevent conflicts.
3. **Fetch Dataset Exports**: Retrieves available datasets from Salesforce.
4. **Process and Save Datasets**: Downloads each dataset in parts and saves them as CSV files, splitting them into chunks of 100,000 rows for manageability.

## Notes

- Ensure your Salesforce account has the necessary permissions to access and export datasets.
- The `salesforce.py` file should be in the same directory as `extract_salesforce_data.robot` to ensure proper import and function execution.
- Adjust the output directory path in the `Clear Old Files` and `Process And Save Dataset` functions if you prefer a different location for the CSV files.

By following this setup, you can automate the extraction of datasets from Salesforce, facilitating efficient data management and analysis.
