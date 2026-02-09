# Wikipedia-University-Data-Pipeline
An automated data engineering project that scrapes university information from Wikipedia and loads structured data into PostgreSQL, MySQL, and SQL Server using Python, SQL, and Docker.



## Project Overview

This project was developed as an end-to-end data engineering case study focused on automating the extraction and storage of large-scale university data from Wikipedia. The objective was to eliminate manual data collection by building a reliable, scalable ETL pipeline capable of harvesting structured university information and loading it into multiple relational database systems.

The project demonstrates practical data engineering skills, including web scraping, data transformation, multi-database integration, and containerized infrastructure using Docker. The data source for this project is Wikipedia’s *List of Largest Universities* page, which provides publicly available information on major universities worldwide.

---

## Project Features

* Automated web scraping of large-scale university data from Wikipedia
* End-to-end ETL pipeline built with Python
* Data cleaning and transformation using Pandas
* Standardized relational schema across multiple databases
* Multi-database integration (PostgreSQL, MySQL, SQL Server)
* Containerized database environments using Docker and Docker Compose
* SQL-based data validation and CRUD operations
* Reproducible and scalable project structure suitable for analytics

---

## Data Design and Schema

The project uses a standardized relational schema to ensure consistency across all supported database systems. The primary table includes the following fields:

* **Universities**: Stores structured information for each university, including name, location, founding year, enrollment size, institution type, and reference URLs.

The schema was designed to support scalability, cross-database compatibility, and analytical querying.

---

## Troubleshooting & Common Errors

### 1. BeautifulSoup Deprecation Warnings

**Issue:** Deprecated `findAll()` method warnings.

**Resolution:** Replaced deprecated methods with `find_all()` to align with modern BeautifulSoup standards.

---

### 2. Regex Syntax Warnings (Invalid Escape Sequence)

**Issue:** `SyntaxWarning: invalid escape sequence '\\d'` when extracting numeric values.

**Resolution:** Used raw string notation for all regular expressions to ensure correct pattern parsing.

---

### 3. SQL Server Connection Issues

**Issue:** Connection failures when integrating SQL Server via Python.

**Resolution:** Verified correct ODBC driver installation, explicitly configured `pyodbc` connections, and passed the active connection into SQLAlchemy using a custom connection creator.

---

### 4. Data Type Conversion Errors

**Issue:** Numeric fields such as enrollment contained commas or missing values.

**Resolution:** Cleaned numeric strings, removed separators, and applied nullable integer types to safely handle missing data.

---

### 5. Docker Container Readiness

**Issue:** Python scripts attempted database connections before containers were fully initialized.

**Resolution:** Added connection retry logic and ensured containers were fully running before executing ETL scripts.

---

## Project Files

* **`scripts_py`**: Python scripts for scraping university data from Wikipedia
* **`data files`**: universities data extracted from wikipedia 
* **`sql`**: All SQL script defining the database schema
* **`docker-compose.yml`**: Docker configuration for multi-database setup
* **`requirements.txt`**: Python dependencies required to run the project
* **`README.md`**: Project documentation

---

## Designing and Implementing the Data Pipeline

To build an efficient and scalable solution, I began by analyzing the structure of Wikipedia’s *List of Largest Universities* page to identify consistent, extractable fields. Using Python’s Requests and BeautifulSoup libraries, I developed a web scraping module capable of reliably extracting structured university data.

The scraped data was then cleaned and transformed using Pandas, addressing inconsistencies such as missing values, formatting issues, and numeric conversions. A standardized relational schema was designed to ensure compatibility across PostgreSQL, MySQL, and SQL Server.

To support reproducible environments and cost-efficient infrastructure, all database systems were containerized using Docker and orchestrated with Docker Compose. Python-based ETL scripts were developed to load the cleaned data into each database while maintaining schema consistency and data integrity.

After data ingestion, I validated the results using SQL queries to confirm record counts, data accuracy, and schema integrity. These queries demonstrated how the dataset could support analytical use cases such as ranking universities by enrollment size or analyzing geographic distribution.

This project showcases my ability to design, implement, and document a production-style data pipeline, highlighting skills in data engineering, database management, and automation.

---

## How to Run This Project

1. Clone the repository

```bash
git clone https://github.com/your-username/wikipedia-university-data-pipeline.git
cd wikipedia-university-data-pipeline
```

2. Create and activate a Python virtual environment, then install dependencies

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\\Scripts\\activate
pip install -r requirements.txt
```

3. Start database services using Docker

```bash
docker-compose up -d
```

4. Run the web scraping script

```bash
python extract.py
python cleaning.py
```

5. Load data into the databases

```bash
python postgres-load.py
python mysql-load.py
python sqlserver=load.py
```

6. Verify loaded data using SQL clients or database management tools


## Data Source

* Wikipedia – *List of Largest Universities*


## License

This project is licensed under the MIT License.
