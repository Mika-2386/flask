import pandas as pd

def clean_data(df):
    df = df.drop_duplicates()
    df = df.fillna(df.mean(numeric_only=True))
    return df

def analyze_data(df):
    mean = df.mean(numeric_only=True).to_dict()
    median = df.median(numeric_only=True).to_dict()
    corr = df.corr().to_dict()
    return mean, median, corr