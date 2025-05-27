### 📄 app.py

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from utils.fetch_data import load_csv_dataset, generate_dummy_data
from utils.sentiment import analyze_sentiment

if "page" not in st.session_state:
    st.session_state.page = "upload_or_generate"

if "df" not in st.session_state:
    st.session_state.df = None

st.set_page_config(page_title="Sentiment Analysis Dashboard", layout="wide")
st.title("Social Media Sentiment Analyzer")

#helper function for feed view
def show_social_feed(df):
    st.markdown("## Live Feed")
    
    emoji_map = {
        "Joy": "😄", "Anger": "😠", "Sadness": "😢",
        "Surprise": "😲", "Disgust": "🤢", "Neutral": "😐", "Positive": "😊"
    }

    for idx, row in df.head(10).iterrows():
        st.markdown("---")
        st.markdown(
            f"""
            **{row['Username']}** • 📍 *{row['Location']}*  
            ⭐ **{row['Rating']:.1f}** &nbsp;&nbsp; {emoji_map.get(row['PredictedSentiment'], '')} **{row['PredictedSentiment']}**  
            *"{row['Text']}"*
            """
        )


# 👣 STEP 1: Upload or Generate Data
import time

# 👣 STEP 1: Upload or Generate Data
if st.session_state.page == "upload_or_generate":
    st.subheader("Upload or Generate Data")

    option = st.radio("Choose Data Source", ["📤 Upload CSV", "🧪 Generate Dummy Data"])

    if option == "📤 Upload CSV":
        uploaded_file = st.file_uploader("Choose a CSV file", type=["csv"], label_visibility="collapsed")
        if uploaded_file:
            df = load_csv_dataset(uploaded_file)
            df = analyze_sentiment(df)
            df.to_csv("datasets/generated.csv", index=False)
            st.session_state.df = df
            st.success(f"✅ Uploaded {len(df)} rows.")
            st.dataframe(df.head())

            # ✅ Download button for raw dataset
            st.markdown("#### 📥 Download Raw Dataset")
            st.download_button(
                label="Download Raw CSV",
                data=df.to_csv(index=False),
                file_name="raw_dataset.csv",
                mime="text/csv",
                use_container_width=True,
                key="download_raw_upload"
            )

            # Proceed
            if st.button("➡️ Proceed to Sentiment Analysis", use_container_width=True, key="proceed_upload"):
                st.session_state.page = "sentiment_analysis"
                st.rerun()

            df = analyze_sentiment(df)
            show_social_feed(df)

    elif option == "🧪 Generate Dummy Data":
        col1, col2 = st.columns([3, 1])
        with col1:
            num_samples = st.slider("Number of Samples", 10, 500, 100)
        with col2:
            generate = st.button("🚀 Generate", use_container_width=True)

        if generate:
            # Add 5-second loading time
            with st.spinner('Generating data, please wait...'):
                time.sleep(10)  # Simulate 5 seconds of loading

            # After the delay, generate data
            df = generate_dummy_data(num_samples)
            df.to_csv("datasets/generated.csv", index=False)
            st.session_state.df = df
            st.success(f"✅ Generated {len(df)} dummy records.")
            st.dataframe(df.head())

            # ✅ Download button for raw dummy dataset
            st.markdown("#### 📥 Download Raw Dataset")
            st.download_button(
                label="Download Raw CSV",
                data=df.to_csv(index=False),
                file_name="raw_dummy_dataset.csv",
                mime="text/csv",
                use_container_width=True,
                key="download_raw_generate"
            )

            # 👉 Proceed button
            if st.button("➡️ Proceed to Sentiment Analysis", use_container_width=True, key="proceed_generate"):
                st.session_state.page = "sentiment_analysis"
                st.rerun()

            # 👉 Analyze and show feed
            df = analyze_sentiment(df)
            show_social_feed(df)

    if st.session_state.df is not None:
        st.markdown("---")
        if st.button("➡️ Proceed to Sentiment Analysis", use_container_width=True):
            st.session_state.page = "sentiment_analysis"


#sentiment analysis page

# 👣 STEP 2: Analyze and Visualize
elif st.session_state.page == "sentiment_analysis":
    st.title("📊 Sentiment Analysis Results")

    if st.session_state.df is not None:
        df = st.session_state.df
    else:
        try:
            df = pd.read_csv("datasets/generated.csv")
            df = analyze_sentiment(df)
        except FileNotFoundError:
            st.warning("No dataset found. Please upload or generate a dataset first.")
            st.stop()

    # Charts
    emotion_counts = df["PredictedSentiment"].value_counts()

    st.write("### Emotion Distribution")

    # 👇 Use columns for bar chart and action buttons
    bar_col, btn_col = st.columns([3, 2])

    with bar_col:
        st.bar_chart(emotion_counts, use_container_width=True)

    with btn_col:
        st.markdown("#### 📥 Download Analyzed Dataset")
        st.download_button(
            label="Download CSV",
            data=df.to_csv(index=False),
            file_name="analyzed_reviews.csv",
            mime="text/csv",
            use_container_width=True
        )

        st.markdown("#### 🔙 Back to Data Generator")
        st.button("Go Back", use_container_width=True, on_click=lambda: st.session_state.update(page="upload_or_generate"))

    # Table
    st.write("### Sample Analyzed Data")
    st.dataframe(df[["Username", "Location", "Text", "Rating", "Score", "ExpectedSentiment", "PredictedSentiment"]])




