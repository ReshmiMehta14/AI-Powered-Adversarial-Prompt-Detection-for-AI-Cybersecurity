import os
import re
import pandas as pd
import streamlit as st
import plotly.express as px
import joblib

# Load ML Model and Vectorizer
model = joblib.load('chatbot_model.pkl')
vectorizer = joblib.load('vectorizer.pkl')
class_labels = ['Code Execution', 'Data Exfiltration', 'Prompt Injection', 'Safe Input', 'Social Engineering']

LOG_FILE_PATH = 'logs/prompt_detection.log'

# Custom Styles
st.markdown("""
    <style>
        .reportview-container {
            background-color: #f8f9fa;
        }
        .stButton>button {
            background-color: #007bff;
            color: white;
            border-radius: 10px;
            padding: 10px;
            font-weight: bold;
        }
        .stDataFrame {
            border-radius: 10px;
            overflow: hidden;
        }
        .css-1aumxhk {
            background-color: #e9ecef;
            border-radius: 10px;
        }
        h1, h2, h3 {
            color: #343a40;
        }
    </style>
""", unsafe_allow_html=True)

# Sidebar Navigation
st.sidebar.title("AI Threat Detection & Analysis Hub")
page = st.sidebar.radio("Navigate to:", ["💬 Real-Time Chat", "📜 Example Logs"])

# ML Prediction Function
def predict_attack_type(user_input):
    input_vector = vectorizer.transform([user_input])
    prediction = model.predict(input_vector)[0]
    #confidence_score = model.predict_proba(input_vector).max() * 100
    return class_labels[prediction]

# 📡 Real-Time Chat Section
if page == "💬 Real-Time Chat":
    st.title("💬 Real-Time Prompt Injection Detection")
    st.write("Test user inputs and analyze detection results in real time.")

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    # Chat Input
    user_input = st.text_input("Enter your message:", key="chat_input")
    if st.button("Send"):
        if user_input.strip():
            prediction = predict_attack_type(user_input)
            st.session_state.chat_history.append({
                "User Input": user_input,
                "Prediction": prediction,
            })

            st.success(f"✅ Prediction: {prediction}")

    # Chat History Display
    if st.session_state.chat_history:
        st.write("## 🧾 Chat History")
        chat_df = pd.DataFrame(st.session_state.chat_history)
        st.dataframe(chat_df)

        # Chat Analysis
        st.write("### 📊 Detection Summary for Chat")
        summary_df = chat_df['Prediction'].value_counts().reset_index()
        summary_df.columns = ['Attack Type', 'Count']

        # Color Mapping for Chart
        color_map = {'Safe Input': 'green'}
        for attack_type in summary_df['Attack Type']:
            if attack_type != "Safe Input":
                color_map[attack_type] = 'red'

        # Chart
        fig = px.bar(
            summary_df,
            x='Attack Type',
            y='Count',
            color='Attack Type',
            title="Detection Summary by Attack Type (Chat)",
            color_discrete_map=color_map
        )
        fig.update_traces(width=0.4)
        st.plotly_chart(fig, use_container_width=True)

# 📖 Example Logs Section
elif page == "📜 Example Logs":
    st.title("📜 Example Log Data Preview")
    
    def load_logs(file_path):
        if not os.path.exists(file_path):
            st.error("❗ Log file not found. Please run the detection first.")
            return pd.DataFrame()

        data = []
        try:
            with open(file_path, 'r') as file:
                for line in file:
                    if "HTTP Request" in line:
                        continue
                    match = re.match(r".*? - INFO - User Input: (.*?) \| Detection Result: (.*)", line.strip())
                    if match:
                        user_input = match.group(1).strip()
                        detection_result = match.group(2).strip()
                        user_input = re.sub(r"^User Input:\s*", "", user_input)
                        prediction = predict_attack_type(user_input)
                        data.append({"User Input": user_input, "Prediction": prediction, })
            return pd.DataFrame(data)
        except Exception as e:
            st.error(f"Error reading log file: {e}")
            return pd.DataFrame()

    df = load_logs(LOG_FILE_PATH)

    if not df.empty:
        st.write("### 📄 Log Data")
        st.dataframe(df)

        st.write("### 📊 Detection Summary for Logs")
        summary_df = df['Prediction'].value_counts().reset_index()
        summary_df.columns = ['Attack Type', 'Count']

        color_map = {'Safe Input': 'green'}
        for attack_type in summary_df['Attack Type']:
            if attack_type != "Safe Input":
                color_map[attack_type] = 'red'

        fig = px.bar(
            summary_df,
            x='Attack Type',
            y='Count',
            color='Attack Type',
            title="Detection Summary by Attack Type (Logs)",
            color_discrete_map=color_map
        )
        fig.update_traces(width=0.4)
        st.plotly_chart(fig, use_container_width=True)

        csv_data = df.to_csv(index=False).encode('utf-8')
        st.download_button(label="Download Logs as CSV", data=csv_data, file_name='detection_logs.csv')
