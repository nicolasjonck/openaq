import json
from connect_to_rds import create_sql_connection

# Load the data from the JSON file
with open('dynamodb_data.json') as infile:
    data = json.load(infile)

conn = create_sql_connection()

if conn is not None:
    cursor = conn.cursor()

    insert_query = '''
    INSERT INTO measurements (
        message_id, location_id, location, parameter, value, date_time_utc, date_time_local,
        unit, latitude, longitude, country, city, is_mobile, is_analysis, entity, sensor_type
    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    '''

    for item in data:
        cursor.execute(insert_query, (
            item['message_id'],
            item['location_id'],
            item['location'],
            item['parameter'],
            float(item['value']),  # Convert to float if necessary
            item['date_time_utc'],
            item['date_time_local'],
            item['unit'],
            float(item['coordinates']['latitude']),
            float(item['coordinates']['longitude']),
            item['country'],
            item['city'],
            item['is_mobile'],
            item['is_analysis'],
            item['entity'],
            item['sensor_type']
        ))

    # Commit the changes and close the connection
    conn.commit()
    cursor.close()
    conn.close()

    print("Data loaded into PostgreSQL successfully.")

else:
    print("Failed to create database connection.")
