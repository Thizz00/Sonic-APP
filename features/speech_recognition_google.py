import speech_recognition as sr
import streamlit as st
class SpeechRecognizer:
    def __init__(self, uploaded_file: str):
        """
        A class for speech recognition using the Google Speech Recognition API.

        Args:
            uploaded_file (str): Path to the audio file to be recognized.
        """
        self.uploaded_file = uploaded_file
        self.recognizer = sr.Recognizer()

    def recognize_speech_google(self) -> str:
        """
        Recognizes speech from an audio file using the Google Speech Recognition API.

        Returns:
            str: The recognized text from the audio file.

        Raises:
            ValueError: If an error occurs during speech recognition.
                Possible reasons: unknown value, request error, or other unexpected errors.
        """
        try:
            with sr.AudioFile(self.uploaded_file) as source:
                audio = self.recognizer.record(source)

            text = self.recognizer.recognize_google(audio)
            return text
        except sr.UnknownValueError:
            '''
            raise ValueError("Unable to recognize speech. Make sure your data doesn't include background music.")
            '''
            st.error("Unable to recognize speech. Make sure your data doesn't include background music.")
            st.stop()
        except sr.RequestError:

            '''
            except sr.RequestError as e:
            raise ValueError("An error occurred during speech recognition: {}".format(e))
            '''

            st.error("An error occurred during speech recognition")
            st.stop()
        except:
            st.error("Try importing another file.")
            st.stop()