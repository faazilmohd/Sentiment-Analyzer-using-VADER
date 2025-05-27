from pyspark.sql import SparkSession
from pyspark.sql.functions import udf, col
from pyspark.sql.types import StringType, FloatType
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import random

analyzer = SentimentIntensityAnalyzer()

# Emotion mapper as a normal function
def map_emotion(score, text):
    text_lower = text.lower()
    if score >= 0.6:
        if any(x in text_lower for x in ["wow", "amazing", "surprised"]):
            return "Surprise"
        return "Joy"
    elif 0.2 <= score < 0.6:
        return "Positive"
    elif -0.2 < score < 0.2:
        return "Neutral"
    elif -0.6 < score <= -0.2:
        if any(x in text_lower for x in ["ugh", "gross", "disgusting"]):
            return "Disgust"
        return "Sadness"
    else:
        if any(x in text_lower for x in ["angry", "furious"]):
            return "Anger"
        return random.choice(["Anger", "Disgust"])

# UDFs
def analyze_sentiment_spark(df_spark):
    score_udf = udf(lambda x: float(analyzer.polarity_scores(x)["compound"]), FloatType())
    emotion_udf = udf(lambda score, text: map_emotion(score, text), StringType())

    df_spark = df_spark.withColumn("Score", score_udf(col("Text")))
    df_spark = df_spark.withColumn("PredictedSentiment", emotion_udf(col("Score"), col("Text")))
    
    return df_spark
