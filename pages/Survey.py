# This creates the page for users to input data.
# The collected data should be appended to the 'data.csv' file.
import csv
import streamlit as st
import pandas as pd
import os # The 'os' module is used for file system operations (e.g. checking if a file exists).

# PAGE CONFIGURATION
st.set_page_config(
    page_title="Survey",
    page_icon="📝",
)

# PAGE TITLE AND USER DIRECTIONS
st.title("Data Collection Survey 📝")
st.write("Please fill out the form below to add your data to the dataset.")

# DATA INPUT FORM
# 'st.form' creates a container that groups input widgets.
# The form is submitted only when the user clicks the 'st.form_submit_button'.
# This is useful for preventing the app from re-running every time a widget is changed.
with st.form("survey_form"):
    # Create text input widgets for the user to enter data.
    # The first argument is the label that appears above the input box.
##    category_input = st.text_input("Enter a category:")
##    value_input = st.text_input("Enter a corresponding value:")

    team_input = st.selectbox(
    "What’s your favorite NFL team?",
    ("Arizona Cardinals",
     "Atlanta Falcons",
     "Baltimore Ravens",
     "Buffalo Bills","Carolina Panthers",
     "Chicago Bears",
     "Cincinnati Bengals",
     "Cleveland Browns",
     "Dallas Cowboys",
     "Denver Broncos",
     "Detroit Lions",
     "Green Bay Packers",
     "Houston Texans",
     "Indianapolis Colts",
     "Jacksonville Jaguars",
     "Kansas City Chiefs",
     "Las Vegas Raiders",
     "Los Angeles Chargers",
     "Los Angeles Rams",
     "Miami Dolphins",
     "Minnesota Vikings",
     "New England Patriots",
     "New Orleans Saints",
     "New York Giants",
     "New York Jets",
     "Philadelphia Eagles",
     "Pittsburgh Steelers",
     "San Francisco 49ers",
     "Seattle Seahawks",
     "Tampa Bay Buccaneers",
     "Tennessee Titans",
     "Washington Commanders"),
    index=None,
    placeholder="Choose a team")
    
    watched_input = st.text_input("How many Super Bowls have you watched?")
    points_input = st.text_input("Predict the combined score of the next Super Bowl")
    
##select box for team instead of text to minimize misinputs
##e.g. "KC Chiefs" vs "Chiefs"
##still do text for stats tho
    
    # The submit button for the form.
    submitted = st.form_submit_button("Submit Data")

    # This block of code runs ONLY when the submit button is clicked.
    if submitted:
        with open("data.csv", "a", newline="") as file:
            writer = csv.writer(file)
            watched_text = watched_input.strip()
            points_text = points_input.strip()

            ##this checks for realistic integers
            if team_input is None:
                st.error("Please choose a team.")
            elif not (watched_text.isdigit() and points_text.isdigit()):
                st.error("Please enter whole numbers for both questions.")
            elif int(watched_text) > 100 or int(points_text) > 200:
                st.error("Super Bowls watched must be 0-100 and the score prediction 0-200.")
            else:

                #now write once chekced
                watched_num = int(watched_text)
                points_num = int(points_text)
                writer.writerow([team_input,watched_num,points_num])

                #success message
                st.success("Your data has been submitted!")
                st.write(f"You entered: **Team:** {team_input}, **# of Bowls:** {watched_num}, **Point Prediction:** {points_num}")

# DATA DISPLAY
# This section shows the current contents of the CSV file, which helps in debugging.
st.divider() # Adds a horizontal line for visual separation.
st.header("Current Data in CSV")

# Check if the CSV file exists and is not empty before trying to read it.
if os.path.exists('data.csv') and os.path.getsize('data.csv') > 0:
    # Read the CSV file into a pandas DataFrame.
    current_data_df = pd.read_csv('data.csv')
    # Display the DataFrame as a table.
    st.dataframe(current_data_df)
else:
    st.warning("The 'data.csv' file is empty or does not exist yet.")
