# This creates the page for displaying data visualizations.

import streamlit as st
import pandas as pd
import altair as alt
import json

# PAGE CONFIGURATION
st.set_page_config(
    page_title="Visuals",
    page_icon="📈",
)

# PAGE TITLE
st.title("Data Visualizations 📈")


# PART 1: GRAPHS FROM data.json
st.header("Super Bowl Champions")

##start working w json file
with open("data.json") as file:
    data = json.load(file)

##pull info from json file, iterate like dictionary
rows = []
for year, info in data.items():
    rows.append({
        "year": int(year),
        "team": info["team"],
        "city": info["city"],
        "conference": info["conference"]
    })
##use pandas for data, easier than looping over dict
##can pass directly to pd.DataFrame b/c new dict per row
framedData = pd.DataFrame(rows)

##STATIC + ADVANCED:
##donut chart, total wins by conference
st.header("Wins by Conference")

##altair donut formatting below, but dont need this bc data already framed
##source = pd.DataFrame({
##    "category": [1, 2, 3, 4, 5, 6],
##    "value": [4, 6, 10, 3, 7, 8]
##})
##

##need to condense to just wins and conference tho b/c 
##dont want 20+ sections for pie/donut

conference_counts = framedData.groupby("conference").size().reset_index(name="wins")
##a lot to unpack but basically:
##.groupby("conference") sorts into piles by conference
##.size() counts rows in pile
##.reset_index(name="wins") turns back into columns w/ name wins,
##altair needs columns for graphs

##altair donut format
donut = alt.Chart(conference_counts).mark_arc(innerRadius=50).encode(
    theta = "wins",
    color = alt.Color(
        "conference",
        title = "Conference",
        scale = alt.Scale(domain=["AFC", "NFC"], range=["#D50A0A", "#013369"])
    )
)

st.altair_chart(donut)
##NFC is blue, AFC is red
##checked stack overflow for how to set colors
##original was for line chart but I messed around, seems to work for donut, similar structure


##DYNAMIC:
st.header("Wins Per Team")

team_counts = framedData.groupby("team").size().reset_index(name="wins")
##same as previous graph but team instead of conference:
##.groupby("team") sorts into piles by team
##.size() counts rows in pile
##.reset_index(name="wins") turns back into columns w/ name wins,
##altair needs columns for graphs

all_teams = sorted(team_counts["team"])


if "selected_teams" not in st.session_state:
    st.session_state.selected_teams = ["Kansas City Chiefs", "New England Patriots", "Seattle Seahawks"]
##guard, creates session_state w/ default

##cant use standard multiselect format (below) b/c want session state
##selected_teams = st.multiselect(
##    "Choose teams to compare",
##    all_teams,
##    default=["Kansas City Chiefs", "New England Patriots", "Seattle Seahawks"]
##)

st.multiselect("Choose teams to compare", all_teams, key="selected_teams")
##need to use key= b/c session state

filteredTeams = team_counts[team_counts["team"].isin(st.session_state.selected_teams)]
##only takes selected teams from session state for chart

if filteredTeams.empty:
    st.info("Pick at least one team to see its wins.")
else:
    bar = alt.Chart(filteredTeams).mark_bar().encode(
    x = alt.X("team", title = "Team"),
    y = alt.Y("wins", title = "Super Bowl Wins")
    ).properties(title = "Super Bowl Wins by Team")
    st.altair_chart(bar)
##altair bar format, also need alt.X/Y and .properties for titles 
##learned abt .empty when researching, will definitely implement in future


# PART 2: GRAPHS FROM data.csv
# --- YOUR CODE GOES HERE ---
##NOTE - I seeded the csv file with 20 data points so y'all can
##actually see the graphs and mean/median statistics


##STATIC SCATTER
st.header("Number of Super Bowls Watched vs Predicted Points")

framedSurvey = pd.read_csv("data.csv")

dot = alt.Chart(framedSurvey).mark_circle(size=80, opacity=0.6).encode(
    x=alt.X("super_bowls_watched", title="Super Bowls Watched"),
    y=alt.Y("predicted_points", title="Predicted Points"),
    tooltip=["favorite_team", "super_bowls_watched", "predicted_points"]
).properties(title="Number of Super Bowls Watched vs Predicted Points")
st.altair_chart(dot)



##DYNAMIC HISTO
st.header("Distribution of Predicted Super Bowl Scores")

if "min_watched" not in st.session_state:
    st.session_state.min_watched = 0
##guard, creates session_state w/ default

st.slider(
    "Minimum number of Super Bowls watched:",
    min_value=0,
    max_value=int(framedSurvey["super_bowls_watched"].max()),
    key="min_watched"
)
##need to use key= b/c session state
##give ppl the ability to filter predictions by num of super bowls
##watched, can see data from ppl w/ maybe more experience

filteredSurvey = framedSurvey[
    framedSurvey["super_bowls_watched"] >= st.session_state.min_watched
]
##only takes input w/ min watched from session state for chart

if filteredSurvey.empty:
    st.info("No survey responses match your selection.")

else:
    histogram = alt.Chart(filteredSurvey).mark_bar().encode(
        x=alt.X("predicted_points:Q", bin=True, title="Predicted Combined Points"),
        y=alt.Y("count()", title="Number of Responses"),
        tooltip=["count()"]
    ).properties(title="Distribution of Predicted Super Bowl Scores")

    st.altair_chart(histogram)


    ##trying for extra credit
    ##pandas has mean and media funcs
    
    current_mean = filteredSurvey["predicted_points"].mean()
    current_median = filteredSurvey["predicted_points"].median()

    #this sets defaults like w/ chart 2 using session state
    if "previous_mean" not in st.session_state:
        st.session_state.previous_mean = None

    if "previous_median" not in st.session_state:
        st.session_state.previous_median = None

    ##need to make sure theres data
        
        #display mean or no change
    st.metric("Mean Predicted Points", round(current_mean, 2),
    delta = None if st.session_state.previous_mean is None
    else round(current_mean - st.session_state.previous_mean, 2))

    #display median or no change
    st.metric("Median Predicted Points", round(current_median, 2),
    delta = None if st.session_state.previous_median is None
    else round(current_median - st.session_state.previous_median, 2))


    #update values
    st.session_state.previous_mean = current_mean
    st.session_state.previous_median = current_median


