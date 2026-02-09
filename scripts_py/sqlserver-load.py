# Libraries Used
import pandas as pd
import pyodbc
from sqlalchemy import create_engine


# Database configuration
CONN_STRING = (
    "DRIVER={ODBC Driver 17 for SQL Server};"
    "SERVER=localhost,1435;"
    "UID=sa;"
    "PWD=Wikipediapassword_01"
)

DATABASE_NAME = "Wikipediadb"
CSV_FILE = "universities-clean.csv"
CREATE_TABLE_SQL = "./sql/sqlserver_create_table.sql"
UPSERT_SQL = "./sql/sqlserver_upsert.sql"


def get_connection():
    """Create and return a SQL Server connection."""
    conn = pyodbc.connect(CONN_STRING)
    conn.autocommit = True
    return conn


def load_sql_file(path):
    """Read and return SQL from a file."""
    with open(path, "r") as file:
        return file.read()


def main():
    # Connect to SQL Server
    conn = get_connection()
    cursor = conn.cursor()

    # List databases
    cursor.execute("SELECT name FROM sys.databases;")
    print("Existing databases:")
    print(cursor.fetchall())

    # Create database if it does not exist
    cursor.execute(
        f"""
        IF DB_ID('{DATABASE_NAME}') IS NULL
        CREATE DATABASE {DATABASE_NAME};
        """
    )
    cursor.execute(f"USE {DATABASE_NAME};")
    print(f"Using database: {DATABASE_NAME}")

    
    # Create table
    create_table_sql = load_sql_file(CREATE_TABLE_SQL)
    cursor.execute(create_table_sql)
    print("Table creation script executed.")

    
    # SQLAlchemy engine (for pandas)
    engine = create_engine(
        "mssql+pyodbc://", creator=lambda: conn
    )

    print("\nData BEFORE load:")
    try:
        print(pd.read_sql("SELECT * FROM university;", con=engine).head())
    except Exception:
        print("Table is empty.")

    
    # Load CSV into staging table
    df = pd.read_csv(CSV_FILE)
    print(f"\nLoaded {len(df)} rows from {CSV_FILE}")

    # Write to temporary staging table
    df.to_sql(
        "#staging",
        index=False,
        con=engine,
        if_exists="replace"
    )

    print("\nStaging table preview (France):")
    print(
        pd.read_sql(
            "SELECT * FROM #staging WHERE country = 'France';",
            con=engine
        )
    )

    
    # Upsert into main table
    upsert_sql = load_sql_file(UPSERT_SQL)
    cursor.execute(upsert_sql)
    print("Data upsert completed.")

    # Verify load
    print("\nData AFTER upsert:")
    print(pd.read_sql("SELECT * FROM university;", con=engine).head())

    
    # Cleanup
    cursor.close()
    conn.close()
    print("\nSQL Server connection closed.")


if __name__ == "__main__":
    main()
