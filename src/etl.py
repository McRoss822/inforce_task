import csv
import pandas as pd
import re
from db.models.user_table import insert_data_from_csv
from db.db_init import Base, engine

def csv_read(data_file_pth: str):
    """
    Reads and prints the contents of a CSV file using a custom delimiter and quote character.

    Args:
        data_file_pth (str): Path to the CSV file.
    """
    with open(data_file_pth, newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
        for row in spamreader:
            print(', '.join(row))


def signup_date_transformation(data_file: str, output_file: str):
    """
    Transforms the 'signup_date' column into a standardized YYYY-MM-DD format.

    Args:
        data_file (str): Path to the input CSV file.
        output_file (str): Path to save the transformed CSV.
    """
    df = pd.read_csv(data_file)
    df['signup_date'] = pd.to_datetime(df['signup_date']).dt.strftime('%Y-%m-%d')
    df.to_csv(output_file, index=False)
    print("[CONVERTION] Converted signup_date to YYYY-MM-DD")


def pattern_email_check(email: str) -> bool:
    """
    Validates an email address against custom rules and regex patterns.

    Args:
        email (str): Email address to validate.

    Returns:
        bool: True if email is valid, False otherwise.
    """
    if not isinstance(email, str) or '@' not in email:
        return False

    if email.count('@') != 1:
        return False

    local, domain = email.split('@', 1)

    if not local or not domain:
        return False

    if local[0] == '.' or local[-1] == '.':
        return False

    if '..' in local:
        return False

    local_pattern = r'^[a-zA-Z0-9.!#$%&\'*+/=?^_`{|}~-]+$'
    if not re.fullmatch(local_pattern, local):
        return False

    if domain[0] in '.-' or domain[-1] in '.-':
        return False

    if '..' in domain:
        return False

    domain_pattern = r'^[a-zA-Z0-9-]+(\.[a-zA-Z]{2,})+$'
    if not re.fullmatch(domain_pattern, domain):
        return False

    return True


def invalid_email_filtering(data_file: str, output_file: str):
    """
    Filters out rows with invalid emails and saves only valid rows.

    Args:
        data_file (str): Path to the input CSV file.
        output_file (str): Path to save the filtered CSV.
    """
    df = pd.read_csv(data_file)
    valid_rows = []

    for i, row in df.iterrows():
        email = row['email']
        if pattern_email_check(email):
            valid_rows.append(row)
        else:
            print(f"[INVALID] {email}")

    df_filtered = pd.DataFrame(valid_rows)
    df_filtered.to_csv(output_file, index=False)


def add_domain_column(data_file: str, output_file: str):
    """
    Adds a 'domain' column to the dataset based on the 'email' field.

    Args:
        data_file (str): Path to the input CSV file.
        output_file (str): Path to save the updated CSV with domain column.
    """
    df = pd.read_csv(data_file)
    df['domain'] = df['email'].apply(lambda x: x.split('@')[1] if isinstance(x, str) and '@' in x else '')
    df.to_csv(output_file, index=False)
    print("[EXTRA COLUNM] domain column added")

import os

if __name__ == "__main__":
    """
    Executes the full ETL process:
    - Transforms signup date format
    - Filters invalid emails
    - Adds domain column
    - Initializes DB schema
    - Inserts data into DB
    """

    intermediate_files = [
        'src/data/data_datetime.csv',
        'src/data/data_filtered.csv',
        'src/data/data_domain.csv'
    ]

    for file_path in intermediate_files:
        if os.path.exists(file_path):
            os.remove(file_path)
            print(f"[CLEANUP] Removed: {file_path}")

    signup_date_transformation('src/data/data.csv', 'src/data/data_datetime.csv')
    invalid_email_filtering('src/data/data_datetime.csv', 'src/data/data_filtered.csv')
    add_domain_column('src/data/data_filtered.csv', 'src/data/data_domain.csv')
    Base.metadata.create_all(engine)
    insert_data_from_csv('src/data/data_domain.csv')
