# Importing Libraries:
The code imports necessary libraries such as Streamlit for creating web apps, Altair and Plotly Express for data visualization, pandas and numpy for data manipulation, joblib for loading a machine learning model, and hashlib for password hashing.

# Loading the Model:
A machine learning model (mood_navigator.pkl) is loaded using joblib. This model is responsible for predicting emotions in text.

# Defining Utility Functions:
predict_emotions: This function takes text input and returns the predicted emotion.

get_prediction_proba: This function returns the probability distribution of predicted emotions.

Various functions related to database operations for user authentication and tracking user history.

# Main Application:
- The main application logic is defined in the main() function. This function creates the user interface using Streamlit.
- It handles user authentication, allowing existing users to log in and new users to register.
- It provides options for users to input text and receive predictions about the emotions contained within it.
- It tracks user interactions and history, storing them in a SQLite database.
- It offers a logout option for users to log out of their accounts.

# Streamlit Interface:
The Streamlit interface includes components like text inputs, buttons, and selection boxes to interact with the application. It also displays the results of emotion detection and historical data.

# Database Operations:
The track_utils.py file contains functions for creating tables in a SQLite database and performing operations like adding data and querying data related to page visits, user details, and emotion predictions.


# Installation
1. Clone the repository to your local machine:
```
git clone https://github.com/xpert-codes/Mood-Navigator-Web-App-Using-Machine-Learning-in-Python.git
```

2. Install the 'requirements.txt':
```
pip install -r requirements.txt
```

3. To run this project :
```
streamlit run app.py
```

4. It'll automatically open the Streamlit app in your default browser.
