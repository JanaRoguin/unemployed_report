from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError
from dotenv import load_dotenv
import os
import pandas as pd

# get DB URL from .env
load_dotenv()
DB_URL = os.getenv("DB_URL")

# config connection PostgreSQL
engine = create_engine(DB_URL)

# queries to create tables if don't exist
CREATE_TABLES_QUERY = """
DROP TABLE IF EXISTS candidates;
DROP TABLE IF EXISTS jobs;
DROP TABLE IF EXISTS education;

CREATE TABLE IF NOT EXISTS candidates (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255),
    location VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS jobs (
    id SERIAL PRIMARY KEY,
    candidate_id INT REFERENCES candidates(id),
    current_job BOOLEAN
);

CREATE TABLE IF NOT EXISTS education (
    id SERIAL PRIMARY KEY,
    candidate_id INT REFERENCES candidates(id),
    degree VARCHAR(255)
);
"""

# function to import data from CSV
def import_csv_to_db(engine, table_name, csv_path):
    try:
        df = pd.read_csv(csv_path)
        df.to_sql(table_name, engine, if_exists='replace', index=False)
        print(f"Data import successfully in {table_name}")
    except Exception as e:
        print(f"Error importing {table_name}: {e}")

    try:
        # create tables if they don't exist
        with engine.connect() as connection:
            connection.execute(text(CREATE_TABLES_QUERY))
            print("Tables created.")

        # Import data from CSV
        import_csv_to_db(engine, "candidates", "./data/CANDIDATES.csv")
        import_csv_to_db(engine, "jobs", "./data/JOBS.csv")
        import_csv_to_db(engine, "education", "./data/EDUCATION.csv")


        # query for getting unemployed people and location
        QUERY = """
        WITH unemployed_candidates AS (
            SELECT c.id AS candidate_id, c.location
            FROM candidates c
            LEFT JOIN jobs j ON c.id = j.candidate_id AND j.current_job = TRUE
            WHERE j.candidate_id IS NULL
        )
        SELECT 
            COUNT(*) AS total_unemployed,
            location,
            COUNT(location) AS location_count
        FROM unemployed_candidates
        GROUP BY location
        ORDER BY location_count DESC
        LIMIT 1;
        """

        # execute request
        with engine.connect() as connection:
            result = connection.execute(text(QUERY)).fetchone()
        
        # get values
        total_unemployed, most_common_location, most_common_count = result

        # Generate response
        notification = (
            f"There are {total_unemployed} unemployed people. "
            f"Most unemployers live in{most_common_location} ({most_common_count} people)."
        )
        print(notification)

    except SQLAlchemyError as e:
        print(f"Error with database: {e}")
    except Exception as e:
        print(f"General error: {e}")