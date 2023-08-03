import pandas as pd
import streamlit as st
from collections import Counter
from textblob import TextBlob

class PartOfSpeechConverter:
    """
    Class to convert part-of-speech tags to their full names.
    """
    POS_MAPPING = {
        'CC': 'Coordinating conjunction',
        'CD': 'Cardinal number',
        'DT': 'Determiner',
        'EX': 'Existential there',
        'FW': 'Foreign word',
        'IN': 'Preposition or subordinating conjunction',
        'JJ': 'Adjective',
        'JJR': 'Adjective, comparative',
        'JJS': 'Adjective, superlative',
        'LS': 'List item marker',
        'MD': 'Modal',
        'NN': 'Noun, singular or mass',
        'NNS': 'Noun, plural',
        'NNP': 'Proper noun, singular',
        'NNPS': 'Proper noun, plural',
        'PDT': 'Predeterminer',
        'POS': 'Possessive ending',
        'PRP': 'Personal pronoun',
        'PRP$': 'Possessive pronoun',
        'RB': 'Adverb',
        'RBR': 'Adverb, comparative',
        'RBS': 'Adverb, superlative',
        'RP': 'Particle',
        'SYM': 'Symbol',
        'TO': 'to',
        'UH': 'Interjection',
        'VB': 'Verb, base form',
        'VBD': 'Verb, past tense',
        'VBG': 'Verb, gerund or present participle',
        'VBN': 'Verb, past participle',
        'VBP': 'Verb, non-3rd person singular present',
        'VBZ': 'Verb, 3rd person singular present',
        'WDT': 'Wh-determiner',
        'WP': 'Wh-pronoun',
        'WP$': 'Possessive wh-pronoun',
        'WRB': 'Wh-adverb'
    }

    @staticmethod
    def convert_pos_to_full_name(pos_tag: str) -> str:
        """
        Convert a part-of-speech tag to its full name.

        Args:
            pos_tag (str): The part-of-speech tag.

        Returns:
            str: The full name of the part-of-speech tag, or 'Unknown POS' if not found.
        """
        return PartOfSpeechConverter.POS_MAPPING.get(pos_tag, 'Unknown POS')

class TextAnalyzer:
    """
    Class to analyze text using TextBlob.
    """
    @staticmethod
    def analyze_text_blob(input_text: str) -> tuple:
        """
        Analyze the input text using TextBlob and get part-of-speech counts.

        Args:
            input_text (str): The input text to be analyzed.

        Returns:
            tuple: A tuple containing keywords (list) and part-of-speech counts (dict).
        """
        blob = TextBlob(input_text)
        pos_full_names = [(word, PartOfSpeechConverter.convert_pos_to_full_name(tag)) for word, tag in blob.tags]
        pos_counts = Counter(tag[1] for tag in pos_full_names)
        pos_counts = dict(pos_counts)

        options = list(pos_counts.keys())
        keywords = st.multiselect("Select keywords", options, default=options)

        return keywords, pos_counts

class ChartDrawer:
    """
    Class to draw bar charts for keywords and their part-of-speech counts.
    """
    @staticmethod
    def draw_bar_chart(keywords: list, pos_counts: dict):
        """
        Draw a bar chart based on the provided keywords and their part-of-speech counts.

        Args:
            keywords (list): The list of selected keywords.
            pos_counts (dict): The dictionary containing part-of-speech counts.
        """
        max_columns_per_row = 3
        num_keywords = len(keywords)
        columns_per_row = min(max_columns_per_row, num_keywords)
        values = []

        if num_keywords != 0:
            num_rows = (num_keywords + columns_per_row - 1) // columns_per_row

            rows = []
            for row_index in range(num_rows):
                row = st.columns(columns_per_row)
                for col_index in range(columns_per_row):
                    keyword_index = row_index * columns_per_row + col_index
                    if keyword_index >= num_keywords:
                        break
                    keyword = keywords[keyword_index]
                    value = pos_counts[keyword]
                    values.append(value)
                    row[col_index].metric(keyword, value)
                    rows.append(row)
        else:
            st.write("No data available")

        data = pd.DataFrame({'Tags': keywords, 'Number of Appearances': values})
        st.bar_chart(data.set_index('Tags'), use_container_width=True)