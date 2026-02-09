# Libraries Used
import pandas as pd
import pymysql
from sqlalchemy import create_engine


# Database configuration
DB_CONFIG = {
    "host": "localhost",
    "port": 3307,
    "user": "Wikipediauser",
    "password": "Wikipediauserpassword",
    "database": "Wikipediadb",
}

CSV_FILE = "universities-clean.csv"
CREATE_TABLE_SQL = "./sql/mysql_create_table.sql"
UPSERT_SQL = "./sql/mysql_upsert.sql"


def get_connection():
    """Create and return a MySQL connection."""
    return pymysql.connect(
        host=DB_CONFIG["host"],
        port=DB_CONFIG["port"],
        user=DB_CONFIG["user"],
        password=DB_CONFIG["password"],
        database=DB_CONFIG["database"],
    )


def load_sql_file(path):
    """Read and return SQL from a file."""
    with open(path, "r") as file:
        return file.read()


def main():
    # Load cleaned CSV
    df = pd.read_csv(CSV_FILE)
    print(f"Loaded {len(df)} rows from {CSV_FILE}")

    # Convert dataframe to tuple list for executemany
    data = list(df.itertuples(index=False, name=None))

   
    # Connect to MySQL
    conn = get_connection()
    cursor = conn.cursor()

    # Show existing tables
    cursor.execute("SHOW TABLES;")
    print("Existing tables:", cursor.fetchall())


    # Create table (if not exists)
    create_table_sql = load_sql_file(CREATE_TABLE_SQL)
    cursor.execute(create_table_sql)
    print("Table creation script executed.")


    # SQLAlchemy engine (for reads)
    engine = create_engine("mysql+pymysql://", creator=lambda: conn)

    print("\nData BEFORE upsert:")
    try:
        print(pd.read_sql("SELECT * FROM university;", con=engine).head())
    except Exception:
        print("Table is empty.")

    # Upsert data
    upsert_sql = load_sql_file(UPSERT_SQL)
    cursor.executemany(upsert_sql, data)
    conn.commit()
    print("Data upsert completed.")

    # Verify load
    print("\nData AFTER upsert:")
    print(pd.read_sql("SELECT * FROM university;", con=engine).head())

    # Cleanup
    cursor.close()
    conn.close()
    print("\nMySQL connection closed.")


if __name__ == "__main__":
    main()
