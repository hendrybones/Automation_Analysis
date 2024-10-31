import pandas as pd
import numpy as np
import csv

data = pd.read_csv("../../data/raw/Automation syncs.csv", on_bad_lines='skip')
data.head()

# Check summary and data types
data.info()

 #First, check for non-numeric values in 'id' and 'quotation_id'
data['id'] = pd.to_numeric(data['id'], errors='coerce')  # Convert 'id' to numeric, coercing errors
data['quotation_id'] = pd.to_numeric(data['quotation_id'], errors='coerce')  # Convert 'quotation_id' to numeric

# change data types
data = data.assign(
    id=data['id'].fillna(0).astype(int),  # Fill NaN with 0 and convert to integer
    portal=data['portal'].astype(str),  # Convert 'portal' to string
    quotation_id=data['quotation_id'].fillna(0).astype(int),  # Fill NaN with 0 and convert to integer
    master_airwaybill=data['master_airwaybill'].astype(str),  # Convert 'master_airwaybill' to string
    error_type=data['error_type'].astype(str),  # Convert 'error_type' to string
    error_message=data['error_message'].astype(str),  # Convert 'error_message' to string
    created_at=pd.to_datetime(data['created_at'], errors='coerce'),  # Convert to datetime, coercing errors
    updated_at=pd.to_datetime(data['updated_at'], errors='coerce')  # Convert to datetime, coercing errors
)

# check statistical distribution of numerical values
data.describe()

# handling missing values
data.isnull().sum()

#dropna() removes all rows with missing values.
# handling duplicate values
data.duplicated() # returns true of false
data.drop_duplicates()

# removing Unwanted characters

#Clean the 'error_message' column by removing "Automated Job" followed by a number
data['error_message'] = data['error_message'].str.replace(r"[-\s]*Automated Job\s*#\d+", "", regex=True)
data['error_message'] = data['error_message'].str.replace(r"\(\s*Automated Job\s*#\d+\s*\)", "", regex=True)

# Check the updated 'error_message' column
print(data['error_message'].head())

data.head(3)

# Total number of errors by portal or entity

# Filter for automation_sync error types and count total rows
total_automation_syncs = data[data['error_type'] == 'automation_sync'].shape[0]
#Count the occurrences of each unique value in 'error_type'
error_counts = data['error_type'].value_counts()

# Get the count for 'automation_sync', defaulting to 0 if not present
total_automation_syncs = error_counts.get('automation_sync', 0)

print("Total number of automation syncs:", total_automation_syncs)