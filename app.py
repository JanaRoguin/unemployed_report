from fastapi import FastAPI
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError
from dotenv import load_dotenv
import os

app = FastAPI()

# Function for connecting only when is needed
def get_engine():
    load_dotenv()
    DB_URL = os.getenv("DB_URL")
    return create_engine(DB_URL)

@app.get("/")
def home():
    return {"message": "Welcome to Unemployed Report"}

@app.get("/unemployed-report")
def unemployed_report():
    try:
        engine = get_engine()  # creating connection in the moment

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

        with engine.connect() as connection:
            result = connection.execute(text(QUERY)).fetchone()

        total_unemployed, most_common_location, most_common_count = result

        return {
            "total_unemployed": total_unemployed,
            "most_common_location": most_common_location,
            "most_common_count": most_common_count
        }

    except SQLAlchemyError as e:
        return {"error": f"Error with database: {e}"}
    except Exception as e:
        return {"error": f"General error: {e}"}
