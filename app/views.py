import asyncio
import time

import aiohttp
from django.shortcuts import render

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
