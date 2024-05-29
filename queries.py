from connect_to_rds import create_sql_connection, fetch_data, execute_query
import pandas as pd

def fetch_locations():
    query = "SELECT DISTINCT location FROM measurements"
    return fetch_data(query)

def fetch_parameters():
    query = "SELECT DISTINCT parameter FROM measurements"
    return fetch_data(query)

def fetch_min_date(location):
    query = "SELECT MIN(date_time_utc) AS date_time_utc FROM measurements WHERE location = :location"
    return fetch_data(query, params={"location": location})

def fetch_max_date(location):
    query = "SELECT MAX(date_time_utc) AS date_time_utc FROM measurements WHERE location = :location"
    return fetch_data(query, params={"location": location})

def fetch_param_data(location, param, start_date, end_date):
    start_date = pd.to_datetime(start_date).strftime('%Y-%m-%d %H:%M:%S')
    # Include end date
    end_date = (pd.to_datetime(end_date) + pd.DateOffset(days=1)).strftime('%Y-%m-%d %H:%M:%S')
    query = """
        SELECT location, parameter, value, date_time_utc
        FROM measurements
        WHERE location = :location 
        AND parameter = :parameter 
        AND date_time_utc BETWEEN :start_date AND :end_date;
    """
    return fetch_data(query, params={
        "location": location,
        "parameter": param,
        "start_date": start_date,
        "end_date": end_date
    })

def create_rds_measurement_table():
    query = """
        CREATE TABLE measurements (
            message_id TEXT PRIMARY KEY,
            location_id TEXT,
            location TEXT,
            parameter TEXT,
            value NUMERIC,
            date_time_utc TIMESTAMP,
            date_time_local TIMESTAMP,
            unit TEXT,
            latitude NUMERIC,
            longitude NUMERIC,
            country TEXT,
            city TEXT,
            is_mobile BOOLEAN,
            is_analysis BOOLEAN,
            entity TEXT,
            sensor_type TEXT
        );
    """
    return execute_query(query)