"""
Class: CS230--Section 2
Name: Samantha Hess
Description: FINAL PROJECT: INTERACTIVE DATA-EXPLORER: TELL A STORY WITH REAL-WORLD DATA
I pledge that I have completed the programming assignment independently. 
I have not copied the code from a student or any source.
I have not given my code to any student. 
"""
import matplotlib.pyplot as plt
import streamlit as st
import pandas as pd
import pydeck as pdk
import seaborn as sns


# Read in data
def read_data():
    df = pd.read_csv("RollerCoasters-Geo.csv")

    return df


# Welcome page function - introduce website and include MP4
def welcome_page():
    st.markdown("<h2 style = 'text-align: left; color:blue;'>Welcome to All Things Roller Coasters! </h2>",
                unsafe_allow_html=True)
    st.write(f"Here you will be able to find information and data about roller coasters across the U.S. Enjoy!")
    st.divider()
    st.subheader("Please click through the tabs above to explore.")
    st.markdown("Brought to you by Samantha Hess")
    st.video("WelcomeVideo.mp4")
    ride = st.sidebar.selectbox(
        "**After learning more about inversions, would you ride a roller coaster with inversions?**",
        ("Yes", "No"))
    if ride == "Yes":
        st.sidebar.write("Yay! See you on the roller coasters!")
    elif ride == "No":
        st.sidebar.write("That's too bad. Don't worry, there are other rides to enjoy!")


# Map function - map of all roller coasters in U.S.
def generate_map(df):
    st.markdown("<h2 style = 'text-align: left; color:blue;'>Map of Rollercoasters in the US </h2>",
                unsafe_allow_html=True)
    st.write("Here is a **map** of roller coasters across the U.S. Hover over the pins to learn more about that "
             "coaster!")
    df = df.drop(columns=["Age_Group", "Type", "Design", "Year_Opened", "Top_Speed", "Max_Height", "Drop", "Length",
                          "Duration", "Inversions", "Num_of_Inversions"])
    view_state = pdk.ViewState(
        latitude=df["Latitude"].mean(),
        longitude=df["Longitude"].mean(),
        zoom=3,
        pitch=20)
    map_layout = pdk.Layer("ScatterplotLayer",
                       data=df,
                       get_position="[Longitude, Latitude]",
                       get_radius=12500,
                       get_color=[12, 50, 150],
                       pickable=True)
    dots_info = {"html": "Coaster: {Coaster} <br/> Park: {Park} <br/> City: {City} <br/> State: {State}",
                "style": {"backgroundColor": "white",
                          "color": "blue"}}
    map = pdk.Deck(layers=[map_layout], initial_view_state=view_state, tooltip=dots_info)
    st.pydeck_chart(map)
    return map


# Pie chart function 1 - shows distribution of coasters with inversions and their percentages per inversion amount
def generate_pie_chart1(df):
    st.markdown("<h2 style = 'text-align: left; color:blue;'>All Things Inversions </h2>", unsafe_allow_html=True)
    st.write("The most intense and thrilling roller coasters contain **inversions**.")
    st.image("Inversion.jpg")
    st.caption("Loch Ness Monster, Busch Gardens, Williamsburg, VA")
    if st.checkbox("**Check the box to display the definition of inversion.**"):
        st.write('According to Coaster Force, a **roller coaster inversion** is a roller coaster element that turns '
                 'riders upside down. They are commonly referred to as "loops".')
    st.divider()
    st.subheader("There are many different types of inversions. ")
    inversion_link = "https://coasterforce.com/inversions/"
    st.write("Check out this [link](%s)" % inversion_link, "to learn about the types of inversions.")
    st.divider()
    st.write("Here is a **pie chart** of roller coasters across the U.S. that have an inversion. It displays the the "
             "inversion amount and its percentage.")
    freq_design = df["Num_of_Inversions"].value_counts()
    pie1, axis = plt.subplots()
    axis.pie(freq_design.values, labels=freq_design.index, autopct="%1.1f%%", shadow=True, startangle=90)
    axis.axis("equal")
    axis.set_title("Distribution of Coasters with Inversions and Amounts")
    st.pyplot(pie1)


# Query function 1 - displays the sum of the number of inversions in each park
def inversion_query(df):
    st.divider()
    st.write("Here is a **query** that displays the **sum of the number of inversions in each park**.")
    df_query1 = df.groupby("Park")["Num_of_Inversions"].sum()
    query_sort = df_query1.sort_values(ascending=False)
    table = st.table(query_sort)
    return table


# Bar chart function - shows mean top speeds for each age group, use seaborn to create upscaled bar chart
def generate_bar_chart(df):
    st.write("Here is a **bar chart** that shows the mean top speed for each age group.")
    bar_chart = sns.barplot(data=df, x="Age_Group", y="Top_Speed")
    st.pyplot(bar_chart.figure)


# Pie chart function 2 - shows distribution of roller coaster age groups
def generate_pie_chart2(df):
    st.write("Here is a **pie chart** that shows the distribution of roller coaster age groups.")
    freq_age_group = df["Age_Group"].value_counts()
    pie2, axis = plt.subplots()
    axis.pie(freq_age_group.values, labels=freq_age_group.index, autopct="%1.1f%%", shadow=True, startangle=90)
    axis.axis("equal")
    axis.set_title("Distribution of Coasters by Age Group")
    st.pyplot(pie2)


# Line chart function - shows mean max height of roller coasters by the year they opened
def generate_line_chart(df):
    st.markdown("<h2 style = 'text-align: left; color:blue;'>All Things Height </h2>", unsafe_allow_html=True)
    st.write("Here is a **line chart** of the mean max heights of roller coasters by the year they opened.")
    height = df.groupby("Year_Opened")["Max_Height"].mean().reset_index()
    line, axis = plt.subplots()
    axis.plot(height["Year_Opened"], height["Max_Height"])
    axis.set_title("Mean of Max Height of Coasters by Year Opened")
    axis.set_xlabel("Year Opened")
    axis.set_ylabel("Max Height")
    st.pyplot(line)


# Query function 2 - displays coasters that opened in the year 2000 and have a max height greater than 150
def height_query(df):
    st.divider()
    st.write("Here is a **query** that displays roller coasters which **opened in the year 2000 and have a max height "
             "greater than 150**.")
    df_query2 = df[(df["Year_Opened"] == 2000) & (df["Max_Height"] > 150)]
    table = df_query2[["Coaster", "Park", "Max_Height"]].reset_index(drop=True)
    st.write(table)
    return table


# Title of website
st.markdown("<h1 style = 'text-align: left; color:blue;'>Roller Coasters in the USA </h2>", unsafe_allow_html=True)

# Create tabs for each section of website/data - call functions to each tab
tab1, tab2, tab3, tab4, tab5 = st.tabs(["Welcome", "Map", "All Things Inversions", "All Things Age and Speed",
                                        "All Things Height"])  # Divide pages into tabs to make site more user-friendly

# Welcome page tab
with tab1:
    df = read_data()
    welcome_page()

# Map tab - map
with tab2:
    df = read_data()
    generate_map(df)

# All Things Inversions tab - pie chart, query
with tab3:
    df = read_data()
    generate_pie_chart1(df)
    inversion_query(df)

# All Things Age and Speed tab - bar chart and pie chart
with tab4:
    st.markdown("<h2 style = 'text-align: left; color:blue;'>All Things Age and Speed </h2>", unsafe_allow_html=True)
    st.write("US roller coaster data is separated into **age groups**. Use the slider to learn how the age groups are "
             "divided by year.")
    slider = st.slider("Age Groups", 1, 3)
    if slider == 1:
        st.write('Age Group 1 is the **"older"** age group. It includes coasters that first opened in **1915 to 1979**.')
    elif slider == 2:
        st.write('Age Group 2 is the **"recent"** age group. It includes coasters that first opened in **1980 to 1999**.')
    elif slider == 3:
        st.write('Age Group 3 is the **"newest"** age group. It includes coasters that first opened in **2000 to 2016**.')
    st.divider()
    st.write("Here are both a **pie chart** and a **bar chart**.")
    graphs = ["Bar Chart", "Pie Chart"]
    drop_down = st.selectbox("Select a graph to view it.", graphs)
    if drop_down == "Bar Chart":
        df = read_data()
        generate_bar_chart(df)
    elif drop_down == "Pie Chart":
        df = read_data()
        generate_pie_chart2(df)

# All Things Height tab - line chart, query
with tab5:
    df = read_data()
    generate_line_chart(df)
    height_query(df)
