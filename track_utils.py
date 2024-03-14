import sqlite3
import pytz
from datetime import datetime

# Load Database Packages
conn = sqlite3.connect('./data/data.db', check_same_thread=False)
c = conn.cursor()

IST = pytz.timezone('Asia/Kolkata')  # Indian Standard Time

# Function to create page visited table
def create_page_visited_table():
    c.execute('CREATE TABLE IF NOT EXISTS pageTrackTable(pagename TEXT, timeOfvisit TIMESTAMP)')

# Function to add page visited details
def add_page_visited_details(pagename, timeOfvisit=None):
    if timeOfvisit is None:
        timeOfvisit = datetime.now(IST).strftime("%Y-%m-%d %H:%M:%S")
    else:
        timeOfvisit = timeOfvisit.astimezone(IST).strftime("%Y-%m-%d %H:%M:%S")
    c.execute('INSERT INTO pageTrackTable(pagename, timeOfvisit) VALUES (?, ?)', (pagename, timeOfvisit))
    conn.commit()

# Function to view all page visited details
def view_all_page_visited_details():
    c.execute('SELECT * FROM pageTrackTable')
    data = c.fetchall()
    return data

# Function to create emotion classifier table
def create_emotionclf_table():
    c.execute('CREATE TABLE IF NOT EXISTS emotionclfTable(rawtext TEXT, prediction TEXT, probability NUMBER, timeOfvisit TIMESTAMP)')

# Function to add prediction details
def add_prediction_details(rawtext, prediction, probability, timeOfvisit=None):
    if timeOfvisit is None:
        timeOfvisit = datetime.now(IST).strftime("%Y-%m-%d %H:%M:%S")
    else:
        timeOfvisit = timeOfvisit.astimezone(IST).strftime("%Y-%m-%d %H:%M:%S")
    c.execute('INSERT INTO emotionclfTable(rawtext, prediction, probability, timeOfvisit) VALUES (?, ?, ?, ?)', (rawtext, prediction, probability, timeOfvisit))
    conn.commit()

# Function to view all prediction details
def view_all_prediction_details():
    c.execute('SELECT * FROM emotionclfTable')
    data = c.fetchall()
    return data

# Function to create user table
def create_user_table():
    c.execute('CREATE TABLE IF NOT EXISTS userTable(username TEXT, password TEXT)')

# Function to add user details
def add_user_details(username, password):
    c.execute('INSERT INTO userTable(username, password) VALUES (?, ?)', (username, password))
    conn.commit()

# Function to check user credentials
def check_user_credentials(username, password):
    c.execute('SELECT * FROM userTable WHERE username=? AND password=?', (username, password))
    data = c.fetchone()
    return data

# Function to create user-specific emotion classifier table
def create_user_emotionclf_table(username):
    c.execute(
        f'CREATE TABLE IF NOT EXISTS {username}_emotionclfTable(rawtext TEXT, prediction TEXT, probability NUMBER, timeOfvisit TIMESTAMP)'
    )

# Function to add user-specific prediction details
def add_user_prediction_details(username, rawtext, prediction, probability, timeOfvisit=None):
    table_name = f"{username}_emotionclfTable"
    if timeOfvisit is None:
        timeOfvisit = datetime.now(IST).strftime("%Y-%m-%d %H:%M:%S")
    else:
        timeOfvisit = timeOfvisit.astimezone(IST).strftime("%Y-%m-%d %H:%M:%S")
    c.execute(
        f'INSERT INTO {table_name}(rawtext, prediction, probability, timeOfvisit) VALUES (?, ?, ?, ?)',
        (rawtext, prediction, probability, timeOfvisit),
    )
    conn.commit()

# Function to view user-specific prediction details
def view_user_prediction_details(username):
    table_name = f"{username}_emotionclfTable"
    c.execute(f'SELECT * FROM {table_name}')
    data = c.fetchall()
    return data