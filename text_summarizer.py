import nltk
import string
from heapq import nlargest

class TextSummarizer:
    def __init__(self, text: str):
        """
        Initialize the TextSummarizer object.

        Parameters:
            text (str): The input text to be summarized.
        """
        self.text = text
        self.word_freq = {}
        self.sent_score = {}

    def preprocess_text(self) -> list[str]:
        """
        Preprocess the input text by removing punctuation and stopwords.

        Returns:
            List[str]: The preprocessed text as a list of words.
        """
        nopunc = ''.join(char for char in self.text if char not in string.punctuation)
        processed_text = [word for word in nopunc.split() if word.lower() not in nltk.corpus.stopwords.words('english')]
        return processed_text

    def calculate_word_frequencies(self, processed_text: list[str]) -> None:
        """
        Calculate word frequencies for each word in the processed text.

        Parameters:
            processed_text (List[str]): The preprocessed text as a list of words.
        """
        for word in processed_text:
            self.word_freq[word] = self.word_freq.get(word, 0) + 1

    def calculate_sentence_scores(self, sent_list: list[str]) -> None:
        """
        Calculate sentence scores based on the word frequencies.

        Parameters:
            sent_list (List[str]): List of sentences in the text.
        """
        for sent in sent_list:
            for word in nltk.word_tokenize(sent.lower()):
                if word in self.word_freq:
                    self.sent_score[sent] = self.sent_score.get(sent, 0) + self.word_freq[word]

    def summarize_text(self, length: int = 1) -> str:
        """
        Summarize the input text.

        Parameters:
            length (int): The number of sentences in the summary (default is 1).

        Returns:
            str: The summary of the input text.
        """
        sent_list = nltk.sent_tokenize(self.text)
        processed_text = self.preprocess_text()
        self.calculate_word_frequencies(processed_text)
        self.calculate_sentence_scores(sent_list)
        summary_sents = nlargest(length, self.sent_score, key=self.sent_score.get)
        summary = ' '.join(summary_sents)
        return summary
