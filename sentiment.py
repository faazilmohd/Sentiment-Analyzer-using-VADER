from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import random

analyzer = SentimentIntensityAnalyzer()

def map_emotion(score, text):
    text_lower = text.lower()
    
    if score >= 0.6:
        if "wow" in text_lower or "amazing" in text_lower or "surprised" in text_lower:
            return "Surprise"
        return "Joy"
    elif 0.2 <= score < 0.6:
        return "Positive"
    elif -0.2 < score < 0.2:
        return "Neutral"
    elif -0.6 < score <= -0.2:
        if "ugh" in text_lower or "gross" in text_lower or "disgusting" in text_lower:
            return "Disgust"
        return "Sadness"
    else:  # score <= -0.6
        if "angry" in text_lower or "furious" in text_lower:
            return "Anger"
        return random.choice(["Anger", "Disgust"])

def analyze_sentiment(df, text_col="Text"):
    df["Score"] = df[text_col].apply(lambda x: analyzer.polarity_scores(str(x))["compound"])
    df["PredictedSentiment"] = df.apply(lambda row: map_emotion(row["Score"], row[text_col]), axis=1)
    return df
