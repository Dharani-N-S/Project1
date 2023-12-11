import streamlit as st
import pandas as pd
import mysql.connector
import json

mydb = mysql.connector.connect(host="localhost", user="root", password="myroot")
mycursor = mydb.cursor()
mycursor.execute("USE YOUTUBE_DATABASE")

def fetch_data(channel_name):
    query = f"SELECT * FROM CHANNELS WHERE CHANNEL_NAME = '{channel_name}'"
    df = pd.read_sql_query(query, mydb)
    return df.to_dict(orient='records')

st.title("YouTube Data App")
st.sidebar.title("Menu")

if "channel_names" not in st.session_state:
    st.session_state.channel_names = []

if "selected_channel" not in st.session_state:
	st.session_state.selected_channel = ""
		
if st.sidebar.button("Channels"):
	st.session_state.channel_names.clear()
	mycursor.execute("SELECT CHANNEL_NAME FROM CHANNELS")	
	st.session_state.channel_names.extend([row[0] for row in mycursor.fetchall()])

st.session_state.selected_channel = st.sidebar.selectbox("Select a Channel", options=st.session_state.channel_names)

if st.button("Scrap"):
	st.write(st.session_state.selected_channel)
	scrap_data = fetch_data(st.session_state.selected_channel)
	st.json(scrap_data)

queries = {"1. Names of all videos and their corresponding channels" : 
		   "SELECT video_name, channel_name FROM Videos JOIN Channels ON Videos.channel_id = Channels.channel_id",
           "2. Channels with the most number of videos and their count" : "SELECT channel_name, COUNT(video_id) AS number_of_videos FROM Videos JOIN Channels ON Videos.channel_id = Channels.channel_id GROUP BY channel_name ORDER BY number_of_videos DESC LIMIT 1",
           "3. Top 10 most viewed videos and their respective channels" : "SELECT video_name, view_count, channel_name FROM Videos JOIN Channels ON Videos.channel_id = Channels.channel_id ORDER BY view_count DESC LIMIT 10",
           "4. Comments made on each video and their corresponding video names" : "SELECT video_name, GROUP_CONCAT(comment_text) AS Comments FROM Videos JOIN Comments ON Videos.video_id = Comments.video_id GROUP BY video_name",
           "5. Videos with the highest number of likes and their corresponding channel names" : "WITH ranked_videos AS (SELECT video_name, channel_name, like_count, ROW_NUMBER() OVER(PARTITION BY Channels.channel_id ORDER BY like_count DESC) AS row_num FROM Videos JOIN Channels ON Videos.channel_id = Channels.channel_id) SELECT video_name, like_count AS maximum_likes, channel_name FROM ranked_videos WHERE row_num = 1",
           "6. Total number of likes for each video and their corresponding video names" : "SELECT SUM(like_count) AS total_likes, video_name FROM Videos GROUP BY video_name ORDER BY total_likes DESC",
           "7. Total number of views for each channel and their corresponding channel names" : "SELECT SUM(view_count) AS total_views, channel_name FROM Videos JOIN Channels ON Videos.channel_id = Channels.channel_id GROUP BY channel_name",
           "8. Names of all the channels that have published videos in the year 2022" : "SELECT DISTINCT channel_name FROM Channels JOIN Videos ON Channels.channel_id = Videos.channel_id WHERE YEAR(publishedat) = 2022",
           "9. Average duration of all videos in each channel and their corresponding channel names" : "SELECT channel_name, ROUND(AVG(duration),0) AS average_duration_in_seconds FROM Videos JOIN Channels ON Videos.channel_id = Channels.channel_id GROUP BY channel_name",
           "10. Videos with the highest number of comments and their corresponding channel names" : "SELECT channel_name, number_of_comments, video_name FROM (SELECT c.channel_name, COUNT(co.comment_id) AS number_of_comments, v.video_name, RANK() OVER (PARTITION BY c.channel_id ORDER BY COUNT(co.comment_id) DESC) AS rnk FROM channels c JOIN videos v ON c.channel_id = v.channel_id LEFT JOIN comments co ON v.video_id = co.video_id GROUP BY c.channel_id, v.video_id) ranked WHERE rnk = 1 ORDER BY channel_name"
		  }	

def execute_query(query):
	df = pd.read_sql_query(query, mydb)
	return df

if "queries" not in st.session_state:
    st.session_state.queries = []
	
if "selected_query" not in st.session_state:
	st.session_state.selected_query = ""
	
if st.sidebar.button("Queries"):
	st.session_state.queries.clear()
	st.session_state.queries.extend(queries.keys())
st.session_state.selected_query = st.selectbox("Select a query", options=st.session_state.queries)

if st.button("Execute query"):
	st.write(st.session_state.selected_query)
	result = execute_query(queries[st.session_state.selected_query])
	st.dataframe(result)

mydb.close()