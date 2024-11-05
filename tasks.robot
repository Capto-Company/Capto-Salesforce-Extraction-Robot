*** Settings ***
Library    salesforce.py


*** Variables ***
${username}          your_salesforce_username
${password}          your_salesforce_password
${security_token}    your_salesforce_security_token

*** Tasks ***
Authenticate and Process Salesforce Data
    [Documentation]    Authenticates with Salesforce, clears old CSV files, fetches dataset exports, and processes each dataset.
    ${sf}=    Authenticate Salesforce    ${username}    ${password}    ${security_token}
    Clear Old Files    output
    ${dataset_exports}=    Fetch Dataset Exports    ${sf}
    FOR    ${record}    IN    @{dataset_exports}
        ${dataset_export_id}=    Set Variable    ${record}[Id]
        ${publisher_info}=    Set Variable    ${record}[PublisherInfo]
        Process And Save Dataset    ${sf}    ${dataset_export_id}    ${publisher_info}    output
    END
    Open Output Folder