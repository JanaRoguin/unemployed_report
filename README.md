#This script is written in Python and uses PostgreSQL for the database.

#SQLAlchemy and pgAdmin were used to interact with the database and visualize it, respectively.

#An endpoint was created using FastAPI, which returns the total number of unemployed candidates and the location with the highest number of unemployed people.

#The database environment variables are stored in the .env file, using dotenv.

#Errors are handled using try-except.

#Challenge faced:
Initially, the function used to import data from CSVs was:

df.to_sql(table_name, engine, if_exists='append', index=False)

Issue:
When running the project, the number of unemployed candidates kept increasing by 9 each time. This meant that data was being duplicated instead of being replaced.

Solution:
We replaced "append" with "replace" to ensure that each execution overwrites the data, preventing duplicates.

Final version:

df.to_sql(table_name, engine, if_exists='replace', index=False)

Now, running the script always results in 9 unemployed candidates.


#Running the FastAPI App

To run app.py, you need to install the following libraries:

pip install fastapi uvicorn


#Then, start the server with:

uvicorn app:app --reload

This will start a virtual environment.


#API Endpoint

The script's endpoint is:

http://127.0.0.1:8000/unemployed-report

You can open this URL in your browser to see the response.

Expected response:

{
  "total_unemployed": 9,
  "most_common_location": "Buenos Aires, Buenos Aires Province, Argentina",
  "most_common_count": 9
}

#Interactive API Documentation

FastAPI automatically generates interactive API documentation. You can access it at:

http://127.0.0.1:8000/docs#/default/unemployed_report_unemployed_report_get

Here, you can test the endpoint directly from the browser.
