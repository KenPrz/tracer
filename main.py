"""
Main script to generate an Excel documentation file for a MySQL database.

This script acts as the entry point, handling command-line arguments and
orchestrating the database query and Excel generation processes.
"""
import argparse
import sys
from db_utils import get_tables, get_foreign_key_map
from excel_generator import generate_excel_doc

def parse_arguments():
    """
    Parses command-line arguments required for database connection and output file.

    Returns:
        argparse.Namespace: An object containing the parsed arguments.
    """
    parser = argparse.ArgumentParser(
        description="Generates an Excel documentation file for a MySQL database."
    )
    parser.add_argument(
        '--db_container',
        required=True,
        help='Name of the Docker container running the MySQL database.'
    )
    parser.add_argument(
        '--db_user',
        required=True,
        help='Username for the database connection.'
    )
    parser.add_argument(
        '--db_pass',
        required=True,
        help='Password for the database connection.'
    )
    parser.add_argument(
        '--db_name',
        required=True,
        help='Name of the database to document.'
    )
    parser.add_argument(
        '--output_file',
        default="db_doc.xlsx",
        help='Path and name for the output Excel file. (Default: db_doc.xlsx)'
    )
    return parser.parse_args()

def main():
    """
    Main function to execute the database documentation process.
    """
    try:
        # Parse arguments from the command line
        args = parse_arguments()
        db_container = args.db_container
        db_user = args.db_user
        db_pass = args.db_pass
        db_name = args.db_name
        output_file = args.output_file

        print(f"📊 Generating Excel documentation for database '{db_name}'...")

        # Step 1: Get table names and foreign key relationships
        tables = get_tables(db_container, db_user, db_pass, db_name)
        if not tables:
            print("No tables found in the database. Exiting.")
            sys.exit(1)

        fk_map = get_foreign_key_map(db_container, db_user, db_pass, db_name)

        # Step 2: Generate the Excel workbook
        generate_excel_doc(
            output_file, db_container, db_user, db_pass, db_name, tables, fk_map
        )

        print(f"✅ Database documentation generated: {output_file}")

    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()