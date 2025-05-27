# utils/mock_spark.py

import pandas as pd
from utils.sentiment_helpers import vader_score

class MockSparkSession:
    def read_csv(self, path):
        return MockDataFrame(pd.read_csv(path))

    def createDataFrame(self, data):
        return MockDataFrame(data)


class MockDataFrame:
    def __init__(self, df):
        self.df = df

    def withColumn(self, col_name, func):
        self.df[col_name] = self.df.apply(func, axis=1)
        return self

    def toPandas(self):
        return self.df

    def show(self, n=5):
        print(self.df.head(n))

    def select(self, *cols):
        return MockDataFrame(self.df[list(cols)])

    def filter(self, condition_func):
        return MockDataFrame(self.df[self.df.apply(condition_func, axis=1)])

SparkSession = MockSparkSession()
