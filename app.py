
import pandas as pd
import plotly.figure_factory as ff
import plotly.express as px
import streamlit as st
import plotly.graph_objects as go


st.set_page_config(page_title="Students Scoreboard",
                   page_icon=":bar_chart:", layout="wide")

# Read CsV file


@st.cache
def get_data_from_excel():
    df = pd.read_csv('StudentPerf.csv', index_col=False)
    return df


df = get_data_from_excel()

# Implementing sidebar
st.sidebar.header("Please Filter Here:")
gender = st.sidebar.multiselect(
    "Select the Gender:",
    options=df["gender"].unique(),  # shows Options
    # shows the deafult categories for which data is to be displayed
    default=df["gender"].unique()
)

race = st.sidebar.multiselect(
    "Select the Race according to the groups:",
    options=df["race"].unique(),
    default=df["race"].unique(),
)

PE = st.sidebar.multiselect(
    "Select the Parental Level of Education:",
    options=df["parental_level_education"].unique(),
    default=df["parental_level_education"].unique()
)
PrepC = st.sidebar.multiselect(
    "Select if the person has completed test preparation course or not:",
    options=df["test_prep_course"].unique(),
    default=df["test_prep_course"].unique()
)

df_selection = df.query(
    "gender == @gender & parental_level_education == @PE & test_prep_course==@PrepC"
)
# Selection of data to be displayed on the dashboard
# initially calculations are shown considering all the data


# Main HomePage for the dashboard
st.title(":bar_chart: Marks Dashboard")
st.markdown("##")


average_math_score = round(df_selection['math'].mean(), 1)
average_reading_score = round(df_selection['reading'].mean(), 1)
average_writing_score = round(df_selection['writing'].mean(), 1)

left_column, middle_column, right_column = st.columns(3)
with left_column:
    st.subheader("Average Math Score:")
    st.subheader(f"{average_math_score}")
with middle_column:
    st.subheader("Average Reading Score:")
    st.subheader(f"{average_reading_score}")
with right_column:
    st.subheader("Average Writing Score:")
    st.subheader(f"{average_writing_score}")

st.markdown("""---""")

# Pie chart to get the distribution of different groups inn the data
a = df.groupby('race').count()
labels = a.index
values = a['gender']

colors = ['#04b8a7', '#04877b', '#18968b', '#2beddc', '#76f5ea']

fig_pie = go.Figure(data=[go.Pie(labels=labels, values=values, textinfo='label+percent',
                                 insidetextorientation='radial'
                                 )])
fig_pie.update_traces(hoverinfo='label+percent', textfont_size=15,
                      marker=dict(colors=colors, line=dict(color='#000000', width=0.5)))


# Distplot considering marks of math,writing and reading considering bin size of 5
# distplot contains histogram,kde plot and a rug is displayed
hist_data = [df['math'], df['writing'], df['reading']]
colors = ['#FAEDF0', '#03DAC6', '#CF6679']
Group_labels = ['math', 'writing', 'reading']

fig_dist = ff.create_distplot(
    hist_data, Group_labels, bin_size=5, colors=colors)


# Bar Graph for avg math marks according to different groups
avg_Math_wrt_race = (
    df_selection.groupby(by=["race"]).mean()[
        ["math"]]
)
fig_math = px.bar(
    avg_Math_wrt_race,
    x="math",
    y=avg_Math_wrt_race.index,
    orientation="h",
    title="<b>Average Math score</b>",
    color_discrete_sequence=["#03DAC6"] * len(avg_Math_wrt_race),
    template="plotly_white",
)
fig_math.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    xaxis=(dict(showgrid=False))
)

# Bar graph for avergae reading marks according to the groups

avg_Reading_wrt_race = (
    df_selection.groupby(by=["race"]).mean()[
        ["reading"]]
)
fig_reading = px.bar(
    avg_Reading_wrt_race,
    x="reading",
    y=avg_Reading_wrt_race.index,
    orientation="h",
    title="<b>Average Reading Score</b>",
    color_discrete_sequence=["#03DAC6"] * len(avg_Reading_wrt_race),
    template="plotly_white",
)
fig_reading.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    xaxis=(dict(showgrid=False))
)


# Bar graph for average writing marks according to groups
avg_Writing_wrt_race = (
    df_selection.groupby(by=["race"]).mean()[
        ["writing"]]
)

fig_writing = px.bar(
    avg_Writing_wrt_race,
    x="writing",
    y=avg_Writing_wrt_race.index,
    orientation="h",
    title="<b>Average Writing Score</b>",
    color_discrete_sequence=["#03DAC6"] * len(avg_Writing_wrt_race),
    template="plotly_white",
)
fig_writing.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    xaxis=(dict(showgrid=False))
)

left_column, right_column = st.columns(2)
left_column.plotly_chart(fig_pie, use_container_width=True)
right_column.plotly_chart(fig_dist, use_container_width=True)

st.markdown("""---""")

left_column_2, right_column_2 = st.columns(2)
left_column_2.plotly_chart(fig_math, use_container_width=True)
right_column_2.plotly_chart(fig_reading, use_container_width=True)

st.markdown("""---""")

left_column_3, right_column_3 = st.columns(2)
left_column_3.plotly_chart(fig_writing, use_container_width=True)

# Hiding the footer and other non useful components provided by streamlit by default
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)
