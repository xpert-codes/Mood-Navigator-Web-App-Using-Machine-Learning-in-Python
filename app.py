# app.py
import streamlit as st
import altair as alt
import plotly.express as px
import pandas as pd
import numpy as np
from datetime import datetime
import joblib
import hashlib
from track_utils import (
    create_page_visited_table,
    add_page_visited_details,
    view_all_page_visited_details,
    add_user_details,
    check_user_credentials,
    create_user_table,
    IST,
    create_user_emotionclf_table,
    add_user_prediction_details,
    view_user_prediction_details,
)

# Load Model
pipe_lr = joblib.load(open("./models/mood_navigator.pkl", "rb"))

# Function
def predict_emotions(docx):
    results = pipe_lr.predict([docx])
    return results[0]

def get_prediction_proba(docx):
    results = pipe_lr.predict_proba([docx])
    return results

emotions_emoji_dict = {
    "anger": "😠",
    "disgust": "🤮",
    "fear": "😨😱",
    "happy": "🤗",
    "joy": "😂",
    "neutral": "😐",
    "sad": "😔",
    "sadness": "😔",
    "shame": "😳",
    "surprise": "😮",
}

# Main Application
def main():
    st.title("Mood Navigator App")
    create_page_visited_table()
    create_user_table()

    # Use session_state to persist user data
    if "user_state" not in st.session_state:
        st.session_state.user_state = {
            "username": "",
            "logged_in": False,
        }

    # User Authentication
    username_placeholder = st.empty()
    password_placeholder = st.empty()
    login_button_placeholder = st.empty()

    if not st.session_state.user_state["logged_in"]:
        username = username_placeholder.text_input("Username:")
        password = password_placeholder.text_input("Password:", type="password")
        login_button = login_button_placeholder.button("Login")

        if login_button:
            hashed_password = hashlib.sha256(password.encode()).hexdigest()
            user_data = check_user_credentials(username, hashed_password)

            if user_data:
                st.success("Logged in as {}".format(username))
                create_user_emotionclf_table(username)
                st.session_state.user_state["username"] = username
                st.session_state.user_state["logged_in"] = True
                # Clear login fields after successful login
                username_placeholder.empty()
                password_placeholder.empty()
                login_button_placeholder.empty()
            else:
                st.error("Invalid credentials. Please try again.")

    if not st.session_state.user_state["logged_in"]:
        st.info("New user? Register below.")
        new_username = st.text_input("New Username:")
        new_password = st.text_input("New Password:", type="password")

        if st.button("Register"):
            hashed_new_password = hashlib.sha256(new_password.encode()).hexdigest()
            add_user_details(new_username, hashed_new_password)
            st.success("Registration successful. Please log in.")

    if st.session_state.user_state["logged_in"]:
        # Continue with the existing code for mood detection

        # Add a logout button to reset session state and redirect to login page
        if st.button("Logout"):
            st.session_state.user_state["logged_in"] = False
            st.session_state.user_state["username"] = ""
            st.success("Logged out successfully. Redirecting to login page.")
            st.experimental_rerun()

        choice = st.sidebar.selectbox("Menu", ["Home", "History"])

        if choice == "Home":
            add_page_visited_details("Home", datetime.now(IST))
            st.subheader("Mood Detection in Text")

            with st.form(key="emotion_clf_form"):
                raw_text = st.text_area("Type Here")
                submit_text = st.form_submit_button(label="Submit")

            if submit_text:
                col1, col2 = st.columns(2)

                prediction = predict_emotions(raw_text)
                probability = get_prediction_proba(raw_text)

                add_user_prediction_details(
                    st.session_state.user_state["username"],
                    raw_text,
                    prediction,
                    np.max(probability),
                    datetime.now(IST),
                )

                with col1:
                    st.success("Original Text")
                    st.write(raw_text)

                    st.success("Prediction")
                    emoji_icon = emotions_emoji_dict[prediction]
                    st.write("{}: {}".format(prediction, emoji_icon))
                    st.write("Confidence: {}%".format((np.max(probability)) * 100))

                with col2:
                    st.success("Prediction Probability")
                    proba_df = pd.DataFrame(probability, columns=pipe_lr.classes_)
                    proba_df_clean = proba_df.T.reset_index()
                    proba_df_clean.columns = ["Moods", "Probability"]

                    fig = alt.Chart(proba_df_clean).mark_bar().encode(x='Moods', y='Probability', color='Moods')
                    st.altair_chart(fig, use_container_width=True)

        elif choice == "History":
            add_page_visited_details("History", datetime.now(IST))
            st.subheader("History")

            with st.expander("Mood Classifier History"):
                df_emotions = pd.DataFrame(
                    view_user_prediction_details(st.session_state.user_state["username"]),
                    columns=["Rawtext", "Prediction", "Probability", "Time_of_Visit"],
                )
                st.dataframe(df_emotions)
                prediction_count = df_emotions['Prediction'].value_counts().rename_axis('Prediction').reset_index(name='Counts')
                pc = alt.Chart(prediction_count).mark_bar().encode(x='Prediction', y='Counts', color='Prediction')
                st.altair_chart(pc, use_container_width=True)

if __name__ == "__main__":
    main()
