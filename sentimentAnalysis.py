
from transformers import AutoTokenizer, AutoModelForSequenceClassification, pipeline
import numpy as np
url=    "ALANZI/imamu_arabic_sentimentAnalysis"

tokenizer = AutoTokenizer.from_pretrained(url)
model = AutoModelForSequenceClassification.from_pretrained(url)
sentiment_analyzer = pipeline("sentiment-analysis", model=model, tokenizer=tokenizer, return_all_scores=True)
def sentiment(complaint):
    scores=sentiment_analyzer(complaint)[0]
    return scores[0]['score'],scores[2]['score'],scores[1]['score'], np.argmax([scores[0]['score'],scores[2]['score'],scores[1]['score']])


