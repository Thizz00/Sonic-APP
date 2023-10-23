from wordcloud import WordCloud
from features.word_processor import WordProcessor

class WordCloudGenerator:
    """
    A class to generate word clouds from input text.

    Attributes:
        input_text (str): The input text for word cloud generation.
        background_theme (str): The background theme for the word cloud.
    """

    def __init__(self, input_text: str, background_theme: str):
        """
        Initializes the WordCloudGenerator instance.

        Args:
            input_text (str): The input text for word cloud generation.
            background_theme (str): The background theme for the word cloud.
        """
        self.input_text = input_text
        self.background_theme = background_theme
        self.processor = WordProcessor(self.input_text)

    def word_cloud_from_input(self) -> WordCloud:
        """
        Generates a word cloud using the input text.

        Returns:
            WordCloud: The generated word cloud.
        """
        words_count = self.processor.process_input_text_blob()
        words = list(words_count.keys())

        # Set the background color for the word cloud
        background_color = self.background_theme if self.background_theme != "Default" else "#0E1117"

        wordcloud = WordCloud(
            background_color=background_color,
            contour_width=1,
            max_font_size=128,
            max_words=len(words),
            collocations=False,
        ).generate(" ".join(words))

        return wordcloud
