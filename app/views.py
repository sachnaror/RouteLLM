import asyncio
import time

import aiohttp
import spacy
from django.shortcuts import render
from textblob import TextBlob
from transformers import pipeline
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# Load spaCy's English model
nlp = spacy.load("en_core_web_sm")

# Transformers coherence model (optional)
coherence_model = pipeline("text-classification", model="distilbert-base-uncased-finetuned-sst-2-english")

# API keys (replace with actual API keys)
OPENAI_API_KEY = "your_openai_api_key"
CLAUDE_API_URL = "your_claude_api_url"
GEMINI_API_URL = "your_gemini_api_url"

# Asynchronous function to fetch responses from each LLM
async def fetch_llm_response(url, data, headers):
    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=data, headers=headers) as response:
            return await response.json()

# Function to route the call to multiple LLMs in parallel
async def route_llm_call(prompt):
    llm_calls = [
        fetch_llm_response(OPENAI_API_KEY, {"prompt": prompt}, {"Authorization": f"Bearer {OPENAI_API_KEY}"}),
        fetch_llm_response(CLAUDE_API_URL, {"text": prompt}, {}),
        fetch_llm_response(GEMINI_API_URL, {"input": prompt}, {})
    ]
    return await asyncio.gather(*llm_calls)

# Custom Scoring System
def score_response(response):
    response_text = response.get("choices")[0].get("text", "")
    fluency_score = check_fluency(response_text)
    coherence_score = check_coherence(response_text)
    length_score = len(response_text)
    humor_keyword_score = 1 if detect_humor_keywords(response_text) else 0
    humor_model_score = 1 if detect_humor_keywords(response_text) else 0
    humor_score = (humor_keyword_score + humor_model_score) / 2
    sentiment_score = analyze_sentiment_combined(response_text)
    time_score = 1 / response.get("time_taken", 1)  # Prioritize faster responses

    total_score = (fluency_score * 0.25) + (coherence_score * 0.2) + (length_score * 0.2) + (humor_score * 0.15) + (sentiment_score * 0.1) + (time_score * 0.1)

    return total_score

def select_best_response(responses):
    scored_responses = []
    llm_names = ['OpenAI', 'Claude', 'Gemini']  # Names corresponding to LLMs
    for idx, response in enumerate(responses):
        start_time = time.time()
        score = score_response(response)
        scored_responses.append((score, response, llm_names[idx]))  # Append LLM name

    # Return the response with the highest score and its LLM name
    return max(scored_responses, key=lambda x: x[0])[1], max(scored_responses, key=lambda x: x[0])[2]

# Django view
def index(request):
    if request.method == "POST":
        prompt = request.POST.get("prompt")
        responses = asyncio.run(route_llm_call(prompt))
        best_response, winner_llm = select_best_response(responses)
        return render(request, "index.html", {"response": best_response, "winner_llm": winner_llm})  # Include the winner LLM

    return render(request, "index.html")

# Fluency Check with spaCy
def check_fluency(response_text):
    doc = nlp(response_text)
    num_sentences = len(list(doc.sents))
    num_tokens = len(doc)
    if num_sentences == 0 or num_tokens == 0:
        return 0  # Bad fluency score
    return num_tokens / num_sentences  # The higher the better

# Coherence Check with Transformers (Optional)
def check_coherence(response_text):
    result = coherence_model(response_text)
    sentiment = result[0]['label']
    if sentiment == 'POSITIVE':
        return 1
    else:
        return 0

# Humor detection function
HUMOR_KEYWORDS = ["funny", "joke", "haha", "lol", "lmao", "rofl", "pun", "comedy", "humor"]

def detect_humor_keywords(response_text):
    """Check for humor based on predefined keywords."""
    humor_count = sum(1 for word in HUMOR_KEYWORDS if word in response_text.lower())
    return humor_count > 0  # Return True if humor is detected

def analyze_sentiment_combined(response_text):
    """
    Perform sentiment analysis using both TextBlob and VADER,
    and return the average sentiment score.
    """
    # TextBlob Sentiment Analysis
    blob = TextBlob(response_text)
    textblob_sentiment = blob.sentiment.polarity  # Scale: -1 (negative) to 1 (positive)

    # VADER Sentiment Analysis
    vader_sentiment = analyzer.polarity_scores(response_text)['compound']  # Scale: -1 to 1

    # Combine both scores by averaging
    combined_sentiment = (textblob_sentiment + vader_sentiment) / 2

    return combined_sentiment
