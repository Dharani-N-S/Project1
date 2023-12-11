# Project1
YouTube Data Harvesting and Warehousing

Project Overview:
This project focuses on creating a Streamlit application to access and analyze data from given 10 YouTube channels. Users can select a YouTube channel from the dropdown provided and get the relevant information about that particular channel. The data are retrieved using the Google API, stored in a MongoDB data lake, and later migrated to a MySQL data warehouse. The application offers features such as searching and retrieving data from the SQL database, including options for performing various queries.

Problem Statement:
The primary goal is to develop a user-friendly interface for:
Retrieving data from YouTube channels (Channel name, subscribers, video count, playlist ID, video ID, likes, comments, etc.,).
Storing data in a MongoDB data lake.
Migrating data from the data lake to a MySQL data warehouse.
Retrieve data from the SQL database.

Uploaded file details:
1. Project1.ipynb - code for retrieving data from YouTube using Google API
                    code for storing it in MongoDB
                    code for migrating data from MongoDB to MySQL data warehouse
2. Project1_App.ipynb - code for a few changes in MySQL database
                        code to run the Streamlit file Project1_st.py
3. Project1_st.py - code for retrieving data from MySQL database using queries
                    code for Streamlit App
