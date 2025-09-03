"""
Utility functions for interacting with a MySQL database.

This module provides functions to execute MySQL queries within a Docker container
and retrieve key database schema information such as table names and foreign keys.
"""
import subprocess
import sys

def run_mysql(db_container, db_user, db_pass, db_name, query):
    """
    Executes a MySQL query inside the specified Docker container.

    Args:
        db_container (str): The name of the Docker container.
        db_user (str): The database username.
        db_pass (str): The database password.
        db_name (str): The name of the database.
        query (str): The MySQL query to execute.

    Returns:
        str: The standard output from the MySQL command.
    
    Raises:
        subprocess.CalledProcessError: If the MySQL command fails.
    """
    cmd = [
        "docker", "exec", "-i", db_container,
        "mysql", "-u", db_user, f"-p{db_pass}",
        "--batch", "--skip-column-names", db_name,
        "-e", query
    ]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True, encoding='utf-8')
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"Error running MySQL command: {e}")
        print(f"Stdout: {e.stdout}")
        print(f"Stderr: {e.stderr}")
        raise
    except FileNotFoundError:
        print("Error: 'docker' command not found. Is Docker installed and in your PATH?")
        sys.exit(1)

def get_tables(db_container, db_user, db_pass, db_name):
    """
    Retrieves a list of all table names from the specified database.

    Args:
        db_container (str): The name of the Docker container.
        db_user (str): The database username.
        db_pass (str): The database password.
        db_name (str): The name of the database.

    Returns:
        list: A list of table names.
    """
    query = "SHOW TABLES;"
    tables_str = run_mysql(db_container, db_user, db_pass, db_name, query)
    return tables_str.split("\n")

def get_foreign_key_map(db_container, db_user, db_pass, db_name):
    """
    Builds a map of foreign key relationships for the database.

    The map is structured as `(table_name, column_name) -> (referenced_table, referenced_column)`.

    Args:
        db_container (str): The name of the Docker container.
        db_user (str): The database username.
        db_pass (str): The database password.
        db_name (str): The name of the database.

    Returns:
        dict: A dictionary mapping foreign key columns to their referenced tables/columns.
    """
    query = f"""
    SELECT TABLE_NAME, COLUMN_NAME, REFERENCED_TABLE_NAME, REFERENCED_COLUMN_NAME
    FROM INFORMATION_SCHEMA.KEY_COLUMN_USAGE
    WHERE TABLE_SCHEMA = '{db_name}' AND REFERENCED_TABLE_NAME IS NOT NULL;
    """
    fk_rows = run_mysql(db_container, db_user, db_pass, db_name, query).split("\n")

    fk_map = {}
    for row in fk_rows:
        if not row.strip():
            continue
        try:
            t, col, ref_t, ref_c = row.split("\t")
            fk_map[(t, col)] = (ref_t, ref_c)
        except ValueError:
            # Handle malformed rows or unexpected output
            continue
            
    return fk_map
