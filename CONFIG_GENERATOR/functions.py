import pandas as pd
import os
import re
import sys

#check if the input file exists
def check_input_file_existence(input_excel):
    if not os.path.exists(input_excel):
        raise FileNotFoundError(f"Input file '{input_excel}' not found. Please provide a valid input file.")
    

def validate_field_names(df):
    expected_columns = ['type', 'id', 'interval', 'request url', 'username', 'password',
                         'request method', 'target', 'value', 'hosts', 'target.1', 'service_id',
                         'monitoring_type', 'service_name', 'service_offering_1',
                         'monitoring_type', 'service_name', 'service_offering_1',
                         'application name ', 'service_offering_2', 'platform', 'tribe',
                         'partner id', 'tokenizer', 'field', 'target prefix']
                         
                         
    try:

        for column in expected_columns:
            if column not in df.columns:
                raise ValueError(f"Column '{column}' is missing!.")   

        unexpected_columns = set(df.columns) - set(expected_columns)
        if unexpected_columns:
            raise ValueError(f"Unexpected columns present: {', '.join(unexpected_columns)}") #re-direct for input correction?
    except ValueError as ve:
        print(f"Error in field names: {ve}")
        sys.exit(1)

#check if mandatory fields are present 
def check_mandatory_fields(df):
    mandatory_fields = ['type', 'id', 'interval', 'request url', 'username', 'password', 'request method' ]
    try:
        for field in mandatory_fields:
            if df[field].isnull().any():
                raise ValueError (f"Mandatory field '{field}' contains null value.")
    except ValueError as ve:
        print(f"Mandatory field(s) missing : {ve}")
        sys.exit(1)


def fix_trailing_spaces(df):
    df = df.apply(lambda x:x .map(lambda y : y.strip() if isinstance(y, str) else y))
    
    return df

def check_duplicate_urls(df, master_excel_file=None):
    # A set to keep track of unique URLs in the current sheet
    unique_urls = set()

    master_df = None
    if master_excel_file :
        try:
            master_df = pd.read_excel(master_excel_file, engine='openpyxl')
        except FileNotFoundError:
            print(f"Warning: Master Excel file '{master_excel_file}' not found. Skipping duplicate check against master.")
        except Exception as e:
            print(f"Error loading master sheet: {e}")
            master_df = None

    try:
        for _, row in df.iterrows():
            urls = row['request url'].split(', ')
            for url in urls:
                # Check for duplicate URLs in the current sheet
                if url in unique_urls:
                    raise ValueError(f"Duplicate URL '{url}' found in the input data sheet.")
                unique_urls.add(url)

                # Check for duplicate URLs in the master sheet
                if master_df is not None and url in master_df['request url'].str.split(', ').sum(): # Concatenates a list of all URLs
                    raise ValueError(f"Duplicate URL '{url}' found in the master sheet.")

    except ValueError as ve:
        print(f"Error with duplicate URLs: {ve}")
        sys.exit(1)