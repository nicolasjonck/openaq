import streamlit as st
from queries import fetch_locations, fetch_parameters, fetch_min_date, fetch_max_date, fetch_param_data

locations = fetch_locations()

if not locations.empty:
    selected_location = st.sidebar.selectbox(
        'Select a Location', 
        locations['location'].sort_values()
    )
    
    # Fetch and display data for the selected location
    if selected_location:
        st.title(f"Air Quality Data in {selected_location}")

        calender_start_date = fetch_min_date(selected_location)['date_time_utc'][0]
        calender_end_date = fetch_max_date(selected_location)['date_time_utc'][0]
        start_date = st.sidebar.date_input(
            'Start Date',
            value=calender_start_date,
            min_value=calender_start_date,
            max_value=calender_end_date
        )
        end_date = st.sidebar.date_input(
            'End Date',
            value=calender_end_date,
            min_value=calender_start_date,
            max_value=calender_end_date
        )

        parameters = fetch_parameters()
        for param in parameters['parameter']:
            data = fetch_param_data(selected_location, param, start_date, end_date)
            
            number_of_measurements = len(data)
            average_param_value = round(data['value'].mean(), 2)
            st.header(f"{param} data")
            if not data.empty:
                st.subheader(f"Number of measurements in time period: {number_of_measurements}")
                st.subheader(f"Average value over time period: {average_param_value}")
                st.line_chart(data=data, x='date_time_utc', y='value')
            else:
                st.write(f"No {param} data available for {selected_location}.")
        
else:
    st.write("No locations available.")
