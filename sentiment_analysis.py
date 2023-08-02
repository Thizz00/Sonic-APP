import pandas as pd
import streamlit as st
from collections import Counter
from textblob import TextBlob
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import matplotlib.pyplot as plt

class SentimentAnalysis:
    def __init__(self, input_text: str):
        """
        Initialize SentimentAnalysis object with input_text.

        Parameters:
            input_text (str): The text to be analyzed for sentiment.
        """
        self.input_text = input_text
        self.blob = TextBlob(self.input_text)
        self.score = SentimentIntensityAnalyzer().polarity_scores(self.input_text)

    def count_tags(self) -> Counter:
        """
        Count the occurrences of POS tags in the input_text.

        Returns:
            Counter: A Counter object with POS tag counts.
        """
        pos_counts = Counter(tag[1] for tag in self.blob.tags)
        return pos_counts

    def count_words(self) -> tuple[list[str], list[int]]:
        """
        Count the occurrences of each word in the input_text.

        Returns:
            tuple[list[str], list[int]]: A tuple containing two lists - words and their corresponding counts.
        """
        words_count = self.blob.word_counts
        return list(words_count.keys()), list(words_count.values())

    def categorize_words(self) -> tuple[list[str], list[str], list[str]]:
        """
        Categorize words in the input_text as negatives, neutrals, or positives.

        Returns:
            tuple[list[str], list[str], list[str]]: A tuple containing three lists - negatives, neutrals, and positives.
        """
        words, _ = self.count_words()  # Use count_words() to obtain the words
        negatives = []
        neutrals = []
        positives = []
        for word in words:
            analysis_vader_var = SentimentIntensityAnalyzer().polarity_scores(word)
            if analysis_vader_var['neg'] == 1.0:
                negatives.append(word)
            elif analysis_vader_var['neu'] == 1.0:
                neutrals.append(word)
            elif analysis_vader_var['pos'] == 1.0:
                positives.append(word)
        return negatives, neutrals, positives

    def get_sentiment_labels_sizes(self) -> tuple[list[str], list[int]]:
        """
        Get the sentiment labels and their corresponding sizes based on the input_text sentiment score.

        Returns:
            tuple[list[str], list[int]]: A tuple containing two lists - sentiment labels and their corresponding sizes.
        """
        if self.score['neu'] == 0.0 and self.score['neg'] == 0.0:
            labels = ["Positive"]
            sizes = [round(self.score['pos'] * 100)]
        elif self.score['neu'] == 0.0 and self.score['pos'] == 0.0:
            labels = ["Negative"]
            sizes = [round(self.score['neg'] * 100)]
        elif self.score['pos'] == 0.0 and self.score['neg'] == 0.0:
            labels = ["Neutral"]
            sizes = [round(self.score['neu'] * 100)]
        elif self.score['neu'] == 0.0:
            labels = ["Negative", "Positive"]
            sizes = [round(self.score['neg'] * 100), round(self.score['pos'] * 100)]
        elif self.score['neg'] == 0.0:
            labels = ["Neutral", "Positive"]
            sizes = [round(self.score['neu'] * 100), round(self.score['pos'] * 100)]
        elif self.score['pos'] == 0.0:
            labels = ["Negative", "Neutral"]
            sizes = [round(self.score['neg'] * 100), round(self.score['neu'] * 100)]
        else:
            labels = ["Negative", "Neutral", "Positive"]
            sizes = [round(self.score['neg'] * 100), round(self.score['neu'] * 100), round(self.score['pos'] * 100)]
        return labels, sizes

    def plot_pie_chart(self, labels: list[str], sizes: list[int]) -> plt.figure:
        """
        Plot a pie chart based on the provided labels and sizes.

        Parameters:
            labels (list[str]): A list of labels for the pie chart.
            sizes (list[int]): A list of sizes corresponding to each label.

        Returns:
            plt.figure: The matplotlib figure containing the pie chart.
        """
        option = st.selectbox('Apply the theme: ', plt.style.available)
        plt.style.use(option)
        fig, ax = plt.subplots(figsize=(6, 6))
        fig.set_facecolor('#0E1117')
        plt.tight_layout()
        ax.pie(sizes, labels=labels, wedgeprops={'linewidth': 1.0, 'edgecolor': 'white'}, startangle=90,
               textprops={'color': '#0E1117'})
        ax.legend(fontsize="12", loc="upper right")
        return fig
