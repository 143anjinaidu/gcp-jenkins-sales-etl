
# Import pandas library.
# Pandas is used to read, process, validate, and write CSV files.
import pandas as pd

# Import Path from pathlib.
# Path helps us create file paths that work across operating systems.
import pathlib


# --------------------------------------------------
# BLOCK 1: DEFINE PROJECT FILE PATHS
# --------------------------------------------------

# __file__ represents the location of the current Python file (etl.py).
# resolve() converts it into an absolute path.
# parent gives the directory containing etl.py.
#
# Example:
# F:\gcp-jenkins-sales-etl\etl.py
# becomes:
# F:\gcp-jenkins-sales-etl
BASE_DIR = pathlib.Path(__file__).resolve().parent


# Define the location of the input CSV file.
# / joins the base directory with the data folder and sales.csv.
#
# Final path:
# F:\gcp-jenkins-sales-etl\data\sales.csv
INPUT_FILE = BASE_DIR / "data" / "sales.csv"


# Define where the valid records will be saved.
# This file will be created after ETL execution.
PROCESSED_FILE = BASE_DIR / "processed_sales.csv"


# Define where the invalid records will be saved.
# This file will contain records that fail validation.
REJECTED_FILE = BASE_DIR / "rejected_sales.csv"


# --------------------------------------------------
# BLOCK 2: CREATE THE ETL FUNCTION
# --------------------------------------------------

# def is used to define a Python function.
# run_etl() contains all the steps of our ETL process.
#
# A function allows us to organize code into reusable blocks.
def run_etl():

    # Display a message so we know the ETL process has started.
    print("Starting Sales ETL...")


    # --------------------------------------------------
    # BLOCK 3: EXTRACT - READ THE SOURCE CSV FILE
    # --------------------------------------------------

    # pd.read_csv() reads the CSV file into a Pandas DataFrame.
    #
    # A DataFrame is like a table:
    # - Rows represent sales transactions.
    # - Columns represent order_id, customer, product, etc.
    #
    # df is the variable that stores the input data.
    df = pd.read_csv(INPUT_FILE)


    # --------------------------------------------------
    # BLOCK 4: DEFINE REQUIRED COLUMNS
    # --------------------------------------------------

    # These are the columns that must exist in the source CSV.
    #
    # If even one required column is missing,
    # our ETL process should stop.
    required_columns = [
        "order_id",
        "order_date",
        "customer",
        "product",
        "quantity",
        "price",
        "region"
    ]


    # --------------------------------------------------
    # BLOCK 5: CHECK FOR MISSING COLUMNS
    # --------------------------------------------------

    # Loop through each column in required_columns.
    #
    # if col not in df.columns checks whether that column
    # exists in the input DataFrame.
    #
    # Any missing column is added to the missing_columns list.
    missing_columns = [
        col for col in required_columns
        if col not in df.columns
    ]


    # Check whether the missing_columns list contains anything.
    #
    # If the list is not empty, the source file is missing
    # one or more required columns.
    if missing_columns:

        # raise ValueError stops the ETL and displays an error.
        #
        # Example error:
        # Missing columns: ['quantity', 'price']
        raise ValueError(f"Missing columns: {missing_columns}")


    # --------------------------------------------------
    # BLOCK 6: TRANSFORM - CONVERT DATA TYPES
    # --------------------------------------------------

    # Convert quantity column into numeric values.
    #
    # errors="coerce" means:
    # If a value cannot be converted into a number,
    # Pandas replaces it with NaN (missing value).
    #
    # Example:
    # "2"  becomes 2
    # "ABC" becomes NaN
    df["quantity"] = pd.to_numeric(
        df["quantity"], errors="coerce"
    )


    # Convert price column into numeric values.
    #
    # This allows us to check whether price is greater than zero.
    df["price"] = pd.to_numeric(
        df["price"], errors="coerce"
    )


    # Convert order_date into a proper date format.
    #
    # errors="coerce" converts invalid dates into NaT.
    # NaT means Not a Time, similar to NaN for dates.
    #
    # Example:
    # "2026-11-01" becomes a valid date.
    # "wrong-date" becomes NaT.
    df["order_date"] = pd.to_datetime(
        df["order_date"], errors="coerce"
    )


    # --------------------------------------------------
    # BLOCK 7: VALIDATE THE RECORDS
    # --------------------------------------------------

    # Create a condition to identify valid records.
    #
    # notna().all(axis=1):
    # Checks that all required columns have non-missing values.
    #
    # (df["quantity"] > 0):
    # Quantity must be greater than zero.
    #
    # (df["price"] > 0):
    # Price must be greater than zero.
    #
    # & means AND: all three conditions must be true.
    #
    # The result is a Boolean mask:
    # True  = valid record
    # False = invalid record
    valid_mask = (
        df[required_columns].notna().all(axis=1)
        & (df["quantity"] > 0)
        & (df["price"] > 0)
    )


    # --------------------------------------------------
    # BLOCK 8: SEPARATE VALID AND INVALID RECORDS
    # --------------------------------------------------

    # Select rows where valid_mask is True.
    # These records will go into the processed output.
    #
    # copy() creates a separate DataFrame.
    processed_df = df[valid_mask].copy()


    # Select rows where valid_mask is False.
    # The ~ symbol means NOT.
    #
    # Therefore, ~valid_mask selects invalid records.
    rejected_df = df[~valid_mask].copy()


    # --------------------------------------------------
    # BLOCK 9: FORMAT THE DATE COLUMN
    # --------------------------------------------------

    # Convert valid dates into YYYY-MM-DD string format.
    #
    # dt.strftime() formats date values.
    #
    # Example:
    # 2026-11-01 00:00:00
    # becomes:
    # 2026-11-01
    processed_df["order_date"] = (
        processed_df["order_date"].dt.strftime("%Y-%m-%d")
    )


    # Apply the same date formatting to rejected records.
    rejected_df["order_date"] = (
        rejected_df["order_date"].dt.strftime("%Y-%m-%d")
    )


    # --------------------------------------------------
    # BLOCK 10: LOAD - SAVE OUTPUT CSV FILES
    # --------------------------------------------------

    # Save valid records into processed_sales.csv.
    #
    # index=False prevents Pandas from adding an extra
    # DataFrame index column to the CSV.
    processed_df.to_csv(
        PROCESSED_FILE, index=False
    )


    # Save invalid records into rejected_sales.csv.
    rejected_df.to_csv(
        REJECTED_FILE, index=False
    )


    # --------------------------------------------------
    # BLOCK 11: DISPLAY ETL SUMMARY
    # --------------------------------------------------

    # len(df) gives the total number of input records.
    print(f"Total records: {len(df)}")


    # len(processed_df) gives the number of valid records.
    print(f"Valid records: {len(processed_df)}")


    # len(rejected_df) gives the number of invalid records.
    print(f"Rejected records: {len(rejected_df)}")


    # Display a completion message.
    print("ETL completed successfully!")


# --------------------------------------------------
# BLOCK 12: PYTHON ENTRY POINT
# --------------------------------------------------

# __name__ is a special Python variable.
#
# When this file is executed directly using:
# python etl.py
#
# Python sets __name__ to "__main__".
#
# This condition calls run_etl() only when this file
# is executed directly, not when imported by another file.
if __name__ == "__main__":

    # Start the ETL process.
    run_etl()
