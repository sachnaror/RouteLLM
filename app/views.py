import asyncio
import time

import aiohttp
import spacy
from django.shortcuts import render
from transformers import pipeline

# Load spaCy's English model
nlp = spacy.load("en_core_web_sm")

# Transformers coherence model (optional)
coherence_model = pipeline("text-classification", model="distilbert-base-uncased-finetuned-sst-2-english")


# API keys (replace with actual API keys)
OPENAI_API_KEY = "haha...API nahi doonga main apna, env mein chupa ke rakhe hain"
CLAUDE_API_URL = "haha...API nahi doonga main apna, env mein chupa ke rakhe hain"
GEMINI_API_URL = "haha...API nahi doonga main apna, env mein chupa ke rakhe hain"

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
    # Example scoring system: length of response, fluency, and speed
    length_score = len(response.get("text", ""))
    # For now, use response time for scoring
    fluency_score = 1  # Placeholder, you can add NLP fluency checks here
    time_score = 1 / response.get("time_taken", 1)  # prioritize faster responses
    return length_score + fluency_score + time_score

def select_best_response(responses):
    scored_responses = []
    for response in responses:
        start_time = time.time()
        score = score_response({"text": response["choices"][0]["text"], "time_taken": time.time() - start_time})
        scored_responses.append((score, response))

    # Return the response with the highest score
    return max(scored_responses, key=lambda x: x[0])[1]

# Django view
def index(request):
    if request.method == "POST":
        prompt = request.POST.get("prompt")
        responses = asyncio.run(route_llm_call(prompt))
        best_response = select_best_response(responses)
        return render(request, "index.html", {"response": best_response})

    return render(request, "index.html")


# Fluency Check with spaCy
def check_fluency(response_text):
    doc = nlp(response_text)
    num_sentences = len(list(doc.sents))
    num_tokens = len(doc)

    # Score based on the number of sentences and proper token usage
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



# List of keywords for detecting humor
HUMOR_KEYWORDS = ["funny", "joke", "haha", "lol", "lmao", "rofl", "pun", "comedy", "humor"]

def detect_humor_keywords(response_text):
    """Check for humor based on predefined keywords."""
    humor_count = sum(1 for word in HUMOR_KEYWORDS if word in response_text.lower())
    return humor_count > 0  # Return True if humor is detected

def score_response(response):
    response_text = response.get("choices")[0].get("text", "")

    # Fluency score from spaCy
    fluency_score = check_fluency(response_text)

    # Coherence score (optional)
    coherence_score = check_coherence(response_text)

    # Length score (for response completeness)
    length_score = len(response_text)

    # Humor detection (using both methods)
    humor_keyword_score = 1 if detect_humor_keywords(response_text) else 0
    humor_model_score = 1 if detect_humor_model(response_text) else 0

    # Combine humor scores (you can assign weights or use one method)
    humor_score = (humor_keyword_score + humor_model_score) / 2

    # Example time score (based on response time)
    time_score = 1 / response.get("time_taken", 1)  # Prioritize faster responses

    # Combine the scores with weighting (adjust weights as necessary)
    total_score = (fluency_score * 0.3) + (coherence_score * 0.2) + (length_score * 0.2) + (humor_score * 0.2) + (time_score * 0.1)

    return total_score
