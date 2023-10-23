FROM python:3.9

WORKDIR /Sonic-APP

COPY requirements.txt /Sonic-APP

RUN pip install --no-cache-dir -r requirements.txt

RUN [ "python", "-c", "import nltk; nltk.download('all')" ]

COPY . /Sonic-APP

CMD ["streamlit", "run", "main.py"]
