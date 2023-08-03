import streamlit as st
import nltk
from pathlib import Path
import matplotlib.pyplot as plt
from deep_translator import GoogleTranslator
from text_analyzer import TextAnalyzer, ChartDrawer
from sentiment_analysis import SentimentAnalysis
from text_summarizer import TextSummarizer
from word_cloud_generator import WordCloudGenerator
from word_processor import WordProcessor
from speech_converter import SpeechConverter
from speech_recognition_google import SpeechRecognizer

nltk.download('stopwords')


class SpeechToTextApp:
    def __init__(self):
        """
        Initializes the SpeechToTextApp class and sets up the Streamlit application.
        """
        st.set_page_config(page_title="Speech-to-Text Transcription App", page_icon="⚙️", layout="wide")
        st.set_option('deprecation.showPyplotGlobalUse', False)
        current_dir = Path(__file__).parent if "__file__" in locals() else Path.cwd()
        css_file = current_dir / "styles" / "main.css"
        with open(css_file) as f:
            st.markdown("<style>{}</style>".format(f.read()), unsafe_allow_html=True)
            st.markdown("<h1 style='text-align: center;'>Sonic speech2text</h1>", unsafe_allow_html=True)
        self.line_edit: str = None

    def layouts(self, text: str):
        """
        Creates different layout tabs for the Streamlit application.

        Args:
            text (str): The input text to be processed.

        Returns:
            None
        """
        if text:
            translated_line_edit = GoogleTranslator(source='auto', target='en').translate(text)
            tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs(["Translator to en", "POS", "WordsCount", "Wordcloud",
                                                                "Sentiment analyzer", "Summary", "Text to speech"])
            with tab1:
                if translated_line_edit == text:
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.write("")
                    with col2:
                        st.header("Text: ")
                        st.write(translated_line_edit)
                    with col3:
                        st.write("")
                else:
                    col1, col2 = st.columns(2)
                    with col1:
                        st.header("Before translate")
                        st.write(text)
                    with col2:
                        st.header("After translate")
                        st.write(translated_line_edit)

            with tab2:
                keywords, pos_counts = TextAnalyzer.analyze_text_blob(translated_line_edit)
                ChartDrawer.draw_bar_chart(keywords, pos_counts)

            with tab3:
                processor = WordProcessor(translated_line_edit)
                words_count = processor.process_input_text_blob()
                processor.generate_bar_chart(words_count)

            with tab4:
                option = st.selectbox('Apply the background color: ',
                                     ('Default', 'White', 'Black', 'Red', 'Yellow', 'Green', 'Orange', 'Purple', 'Blue', 'Pink'))
                wc_generator = WordCloudGenerator(translated_line_edit, option)
                with st.columns(3)[1]:
                    wordcloud = wc_generator.word_cloud_from_input()

                    fig, ax = plt.subplots(figsize=(6, 6))
                    plt.axis('off')
                    plt.tight_layout()
                    plt.imshow(wordcloud, interpolation='bilinear')
                    st.pyplot()

            with tab5:
                sentiment_analysis = SentimentAnalysis(translated_line_edit)
                negatives, neutrals, positives = sentiment_analysis.categorize_words()

                pos_counts = sentiment_analysis.count_tags()

                co1, co2, co3 = st.columns(3)
                with co1:
                    st.metric("Negative", str(round(sentiment_analysis.score['neg'] * 100)) + '%', len(negatives),
                              delta_color="inverse")
                with co2:
                    st.metric("Neutral", str(round(sentiment_analysis.score['neu'] * 100)) + '%', len(neutrals),
                              delta_color="off")
                with co3:
                    st.metric("Positive", str(round(sentiment_analysis.score['pos'] * 100)) + '%', len(positives))

                labels, sizes = sentiment_analysis.get_sentiment_labels_sizes()

                co1, co2, co3 = st.columns(3)
                with co1:
                    st.write("")
                with co2:
                    fig = sentiment_analysis.plot_pie_chart(labels, sizes)
                    st.pyplot(fig)

                with co3:
                    st.write("")

            with tab6:
                if st.button("Summarize"):
                    summarizer = TextSummarizer(translated_line_edit)
                    summary = summarizer.summarize_text()
                    st.write(summary)

            with tab7:
                speed = st.radio('', ('slow', 'fast'))
                if st.button("Click convert to speech"):
                    with st.spinner('Loading...'):
                        if speed == 'slow':
                            speech_converter = SpeechConverter(translated_line_edit, slow=True, lang='en')
                            sound_file = speech_converter.convert_to_speech()
                        elif speed == 'fast':
                            speech_converter = SpeechConverter(translated_line_edit, slow=False, lang='en')
                            sound_file = speech_converter.convert_to_speech()

                        st.audio(sound_file)

    def main(self):
        """
        Main function to run the Streamlit application.
        """
        option = st.selectbox('Transfer data method:', ('Choose', 'From text', 'Upload file'))
        self.line_edit = None

        if option == 'From text':
            self.line_edit = st.text_area('', placeholder="Write a text message", max_chars=5000)
            self.layouts(self.line_edit)

        if option == 'Upload file':
            uploaded_file = st.file_uploader("Select WAV file", type="wav")
            if uploaded_file is not None:
                with st.spinner("Loading..."):
                    recognizer = SpeechRecognizer(uploaded_file)
                    self.line_edit = recognizer.recognize_speech_google()
                    self.layouts(self.line_edit)


if __name__ == "__main__":
    app = SpeechToTextApp()
    app.main()
