# utils/sentiment_helpers.py

from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

analyzer = SentimentIntensityAnalyzer()

def vader_score(text):
    return analyzer.polarity_scores(text)["compound"]

def classify_sentiment(score):
    if score >= 0.5:
        return "Joy"
    elif score <= -0.5:
        return "Anger"
    elif -0.5 < score < 0:
        return "Sadness"
    elif 0 < score < 0.5:
        return "Neutral"
    else:
        return "Neutral"
