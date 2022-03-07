#!/usr/bin/env python
# coding: utf-8

# In[40]:


## Importing libraries for loading data and making graphical representations
import streamlit as st
import pandas as pd
import altair as alt


# In[41]:


## Reading the file to get dataset
filename = "medals(final).xlsx"
data = pd.read_excel(filename, header = 1)


# In[42]:


data= data.dropna()


# In[45]:


st.set_page_config(
    page_title ="OLYMPIC HISTORY DATA EXPLORATION",
    page_icon ="🌍",
    layout="wide",
    initial_sidebar_state ="expanded",
)


# In[46]:


#show_OverallOlympicHistory = st.sidebar.checkbox("Show Olympic history")
show_InteractiveLegend = st.sidebar.checkbox("Show Interactive Legend")
show_MultiLine = st.sidebar.checkbox("Show Multiline highlight")
show_Histogram = st.sidebar.checkbox("Show the histogram according to plot")
show_Distribution = st.sidebar.checkbox("Show the Distribution")
show_SliderByYear = st.sidebar.checkbox("Show the Slider by Year")


# In[47]:


#displaying all the olympic detail in one chart
#using the bar chart format
st.title("OLYMPIC HISTORY ANALYSIS (1976 - 1988)")
st.title("Please select which chart you would like to visualize")
Overall_data = alt.Chart(data).mark_bar().encode(
#setting the x-axis and the y-axis
x ='count(Athlete)',
y ='Sport',
color ='Gender',
#creating tool tip to display all details when hovered over
tooltip =('Country','Year','Athlete','Gender','Medal')
).properties(width =700,height =700,
title ='Olympic history').interactive()
st.subheader("Olympic history")
    
Overall_data


# In[48]:


#Interactive legend
#create a selection feature-making the area interactive
if show_InteractiveLegend:
    selection = alt.selection_multi(fields=['Sport'], bind='legend')
    click_by_sport = alt.Chart(data).mark_area().encode(
    #setting the x axis
    alt.X('Year:N', axis=alt.Axis(domain=False, tickSize=0)),
    #setting the y axis
    alt.Y('count(Medal)', stack='center'),
    #setting the colour scheme
    alt.Color('Sport', scale=alt.Scale(scheme='category20b')),
   opacity=alt.condition(selection, alt.value(1), alt.value(0.2))
    ).add_selection(
    selection
    ).properties(title ='Interactive Legend',width =700,height =700)
    st.subheader("Select each Sport in the legend to view Count of Medal Records of all Sports since 1976")

    click_by_sport


# In[49]:


#Multiline Highlight
#Prompt:trend of the number of Men and women who have participated in the Olypic games and won medals 
if show_MultiLine:
#creating the selection 
    highlight = alt.selection(type='single', on='mouseover',fields=['Gender'], nearest=True)
#setting x and y axis for the chart using altair
    foundation = alt.Chart(data).encode(x='Country',y='count(Medal)', color='Gender:N')
#plotting data points which will display the trend
    plot = foundation.mark_circle().encode(opacity=alt.value(0)).add_selection(highlight).properties(width=900)
#connecting the data points in order to plot lines
    connectors = foundation.mark_line().encode(size=alt.condition(~highlight, alt.value(1), alt.value(3)))
    st.subheader("Hover over the plot to find the comparison of the number of Male and Female participants who have won medals at the Olympic")
    plot + connectors


# In[50]:


##  Grouping by to create 2 new columns used for the graphical representations 

# Total medal count by country 
data['Total Medal count'] = data.groupby('Country')['Medal'].transform('count')

# Medal count distribution by country and gold, silver or bronze
data['Medal count'] = data.groupby(['Country','Medal'])['Medal'].transform('count')

# Athlete count distribution by sport and Gender
data['Athlete count'] = data.groupby(['Sport','Gender'])['Athlete'].transform('count')

# Printing top 5 rows of the dataset 
#data.head()


# In[51]:


## Number of athletes male and female in each sport and their medal count for gold, silver and bronze
if show_Histogram:
    selector = alt.selection_single(empty='all', fields=['Gender'])

    color_scale = alt.Scale(domain=['Men', 'Women'],
                        range=['#1FC3AA', '#8624F5'])

    foundation = alt.Chart(data).properties(width=600,height=650).add_selection(selector)
## right graph
    plots = foundation.mark_point(filled=True, size=200).encode(x=alt.X('Sport'),y=alt.Y('Athlete count'),color=alt.condition(selector,
                        'Gender:N',
                        alt.value('lightgray'),
                        scale=color_scale),
    )

## left graph
    histogram = foundation.mark_bar(opacity=0.5, thickness=100).encode(
        x=alt.X('Medal'),y=alt.Y('Medal count'),color=alt.Color('Gender:N',scale=color_scale)
        ).transform_filter(selector)
    
    st.subheader("Select the point in the plot to find the Count of Male and Female Athletes in each sport who have won medals in each sport")

    plots | histogram


# In[52]:


##hover over the area to find the distrbution of medal in country and then displays the country and exact medal count 
if show_Distribution:
    brush = alt.selection(type='interval')

    foundation = alt.Chart(data).properties(width=700, height=700).add_selection(brush)

    plot = foundation.mark_point().encode(
    #setting the x axis
    x='Total Medal count',
    #setting the y axis
    y='Medal',
    #setting the color scheme
    color=alt.condition(brush, 'Country', alt.value('lightgray'))
    ).add_selection(
    brush)

    bar_chart = foundation.mark_bar().encode(
    #setting the y axis
    y='Country',
    #setting the color scheme
    color='Country',
    #setting the x axis
    x='Total Medal count'
    ).transform_filter(brush)
    st.subheader("Hover over the area to find the distrbution of medal in country and then displays the country and exact medal count ")
    plot & bar_chart


# In[53]:


## Select year to learn about the medal distribution for each sport 
if show_SliderByYear:
# Slider by year 
    slider_year = alt.binding_range(min=1976, max=1988, step=4)
    year = alt.selection_single(name="year", fields=['Year'], bind=slider_year)
# Display chart 
    bar_chart = alt.Chart(data).mark_bar().encode(alt.X('Sport'),alt.Y('Total Medal count'),color = 'Medal'
    ).properties(width=900,height=300,).add_selection(year).transform_filter(year)
    st.subheader("Select year to learn about the medal distribution for each sport ")
    bar_chart


# In[ ]:




