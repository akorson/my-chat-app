import streamlit as st
import langchain
from googlesearch import search
from scholarly import scholarly
import github
import requests
from bs4 import BeautifulSoup
import duckduckgo
from pymongo import MongoClient
import openai
import pymongo
import os

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

# Set up OpenAI API
openai.api_key = os.environ['OPENAI_API_KEY']

# Set up MongoDB
client = pymongo.MongoClient(os.environ['MONGODB_URI'])
db = client['chat_history']

# Define function to store chat history in MongoDB
def store_chat_history(project, message, response):
    chat = {'project': project, 'message': message, 'response': response}
    db.chats.insert_one(chat)

# Define function to get user input
def get_input(prompt):
    user_input = st.text_input(prompt)
    return user_input

# Define function to get OpenAI response
def get_response(message):
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=message,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.7,
    )

    response_text = response.choices[0].text
    return response_text

# Define function to search Google
def google_search(query):
    search_results = search(query, num_results=10)
    return search_results

# Define function to search Google Scholar
def google_scholar_search(query):
    search_query = scholarly.search_pubs(query)
    return search_query

# Define function to search GitHub
def search_github(query):
    results = github.search_repositories(query)
    return results

# Define function to search Bing
def search_bing(query):
    url = "https://www.bing.com/search?q={}".format(query)
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')
    links = []
    for link in soup.find_all('a'):
        href = link.get('href')
        if href.startswith('http'):
            links.append(href)
    return links

# Define function to search DuckDuckGo
def search_duckduckgo(query):
    search_results = duckduckgo.search(query)
    return search_results

# Define function to upload a file
def upload_file():
    uploaded_file = st.file_uploader("Choose a file", type=["txt", "pdf", "docx"])
    if uploaded_file is not None:
        file_contents = uploaded_file.read()
        st.write(file_contents)
        return file_contents
    else:
        return None

# Define function to download a file
def download_file(file_name, file_contents):
    with open(file_name, "w") as f:
        f.write(file_contents)

# Define function to get OpenAI to write a file
def get_file_content(file_name):
    prompt = f"Please write a {file_name}."
    response = get_response(prompt)
    return response

# Define function to get project name from user
def get_project_name():
    project_name = st.text_input("Enter a name for your project:")
    return project_name

# Define function to select a project
def select_project():
    projects = db.chats.distinct("project")
    project_name = st.selectbox("Select a project:", [""] + projects)
    return project_name

# Set up CSS
st.markdown("""
    <style>
        """ + open("style.css").read() + """
    </style>
   
