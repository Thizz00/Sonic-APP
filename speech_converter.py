from io import BytesIO
from gtts import gTTS

class SpeechConverter:
    """
    SpeechConverter class that converts text to speech using the gTTS library.

    Attributes:
        slow (bool): Flag to control the speed of speech.
        lang (str): Language of the speech.

    Methods:
        convert_to_speech(translated_line_edit: str) -> BytesIO:
            Converts the given text to speech and returns the sound file as a BytesIO object.
    """

    def __init__(self, line_edit: str, slow: bool = False, lang: str = 'en'):
        """
        Initialize the SpeechConverter object.

        Args:
            line_edit (str): The text to be converted to speech.
            slow (bool, optional): Flag to control the speed of speech. Default is False.
            lang (str, optional): Language of the speech. Default is 'en'.
        """
        self.line_edit = line_edit
        self.slow = slow
        self.lang = lang
        self.sound_file = BytesIO()

    def convert_to_speech(self) -> BytesIO:
        """
        Convert the given text to speech using the gTTS library.

        Returns:
            BytesIO: The sound file as a BytesIO object.
        """
        tts = gTTS(self.line_edit, slow=self.slow, lang=self.lang)
        tts.write_to_fp(self.sound_file)
        return self.sound_file
