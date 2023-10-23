# Sonic-APP

#### Sonic app is an application that allows the user to analyze text and speech to text analysis. It is based on translation of text into English, analysis of the most commonly used words, division of text into parts of speech, sentiment analysis, text summary, creation of a recording of a given text, as well as building charts to analyze the text entered by the user.



## Build 
Clone the repo:
`git clone https://github.com/Thizz00/Sonic-APP.git`



*Optional:*  You can add your required PyPi packages to the `requirements.txt`

Run docker build:
`docker build -t sonicapp .`

## Run the main script

Run `docker run -it -p 8501:8501 sonicapp` to run `main.py` in Streamlit.

then open [localhost:8501/?name=main](http://localhost:8501/?name=main) in your browser. 

## Streamlit docs

Project docs: https://streamlit.io/docs/

