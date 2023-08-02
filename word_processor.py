import pandas as pd
import streamlit as st
from textblob import TextBlob

class WordProcessor:
    """
    Class to process text using TextBlob and display a bar chart of word appearances.
    """

    def __init__(self, input_text: str):
        """
        Initialize the WordProcessor instance.

        Parameters:
            input_text (str): The input text to process.
        """
        self.input_text = input_text
        self.blob = TextBlob(self.input_text)

    def process_input_text_blob(self) -> dict:
        """
        Process the input text using TextBlob and count the word occurrences.

        Returns:
            dict: A dictionary containing word counts.
        """
        if not self.input_text.strip():
            return {}
        self.blob = TextBlob(self.input_text)
        word_counts = self.blob.word_counts
        return word_counts

    def generate_bar_chart(self, word_counts: dict) -> None:
        """
        Generate and display a bar chart of word appearances.

        Parameters:
            word_counts (dict): A dictionary containing word counts.
        """
        counts = list(word_counts.values())

        max_count = max(counts)
        threshold = st.slider('Show values above:', 1, max_count)

        if threshold:
            filtered_data = [(word, count) for word, count in word_counts.items() if count >= threshold]
        else:
            filtered_data = list(word_counts.items())

        data = pd.DataFrame(filtered_data, columns=['Words', 'Number of Appearances'])
        st.bar_chart(data.set_index('Words'))
