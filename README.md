# RouteLLM: The Ultimate AI Matchmaker 🚀

Ever wondered what happens when Claude Sonnet 3.5, OpenAI o1, GPT-4o, and Gemini walk into a bar? 🍻 Well, welcome to **RouteLLM**—where AI egos clash and only the smartest survive!

## 🧐 What is RouteLLM?

RouteLLM is an innovative application designed to be the ultimate AI matchmaker! Imagine speed dating for AI models, but with a twist of neural networks and zero awkward silences. 🤖✨ Watch as our brainy bots battle it out in a high-stakes showdown, where the best model gets picked to answer your queries.

### Key Features:

1. **Custom Scoring System**: Based on response time, fluency, and humor.
2. **Parallel Execution**: API requests will be made in parallel using asynchronous programming.
3. **User Interface (UI)**: Django and Bootstrap 5 will be used for the front-end.
4. **Fluency Analysis**: Use NLP libraries like spaCy or transformers to check for grammar and coherence in the responses.
5. **Humor Detection**: Analyze responses for humor using keyword detection or advanced models.
6. **Sentiment Analysis**: Add sentiment analysis using a library like TextBlob or VADER to refine the scoring system.

### Explanation of Scoring

- **Fluency Check (check_fluency)**: This function uses spaCy to analyze sentence structure by dividing the response into sentences and tokens. It gives a score based on the number of tokens per sentence. The more well-formed the response (more sentences and tokens), the better the score.

- **Coherence Check (check_coherence)**: Optionally, using transformers, this checks whether the overall sentiment or coherence of the response is positive or negative. If the response seems coherent (positive), it gets a higher score.

- **Combined Score**: The final score combines fluency, coherence, length, and time. You can adjust the weights to emphasize different aspects (e.g., fluency and coherence could be more important than response length).

### Humor Detection

In RouteLLM, we can analyze the generated responses for humorous elements using two approaches:

1. **Keyword Detection**: This simple method looks for predefined humorous keywords or phrases that often indicate humor, such as “funny,” “joke,” “haha,” “LOL,” etc.
2. **Advanced Models**: For more sophisticated humor detection, we can use pre-trained models that classify whether a given text contains humor or not. We can leverage models from libraries like transformers.

### Sentiment Analysis

We implemented Sentiment Analysis using libraries like TextBlob or VADER. Sentiment Analysis will allow us to measure the emotional tone of the responses (positive, negative, or neutral), which can be factored into the scoring system.

- **TextBlob Sentiment**: Returns a polarity value between -1 (negative) and 1 (positive).
- **VADER Sentiment**: Provides a compound score on the same scale.
- **Combined Sentiment Score**: We average the sentiment scores from both libraries to get a combined score.

## How it Works:

1. TextBlob Sentiment returns a polarity value between -1 (negative) and 1 (positive).
2. VADER Sentiment also provides a compound score on the same scale.
3. We average the sentiment scores from both libraries to get a combined sentiment score.

## How would it look a like at the end :

```
├── RouteLLM/
│   ├── requirements.txt
│   ├── db.sqlite3
│   ├── README.md
│   ├── .env
│   ├── manage.py
│   ├── RouteLLM/
│   │   ├── asgi.py
│   │   ├── settings.py
│   │   ├── urls.py
│   │   └── wsgi.py
│   ├── app/
│   │   ├── models.py
│   │   ├── apps.py
│   │   ├── admin.py
│   │   ├── tests.py
│   │   ├── urls.py
│   │   └── views.py
│   │   ├── templates/
│   │   │   └── index.html

```

### To get started with RouteLLM, follow these steps:

### Prerequisites

- I'm not gonna explain this.

### Installation

1. Clone the repository:
```bash
git clone https://github.com/sachnaror/RouteLLM.git
cd RouteLLM
```

2. Create a virtual environment and activate it (i hate to explain this ..but):
```bash
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

3. Install the required packages:
```bash
pip install -r requirements.txt
```

4. Download the spaCy language model:
```bash
python -m spacy download en_core_web_sm
```

5. Run the application:
```bash
python manage.py runserver
```

### Requirements

Check the  `requirements.txt` file first to get RouteLLM running smoothly:

* Django>=4.0
* spacy>=3.0
* openai>=0.27.0
* textblob>=0.15.3
* vaderSentiment>=3.3.2

Add any other dependencies as required.

### Usage

1. Launch the app and head to your browser at http://127.0.0.1:8000/.
2. Sit back, relax, and let the AI showdown commence!
3. Enjoy the witty banter and high-IQ fun as the models compete to impress you!

### Contributing

Feel free to contribute to RouteLLM! Check out the issues for ideas or create a new feature branch for your contributions:
```bash
git checkout -b feature/YourFeatureName
```
Then submit a pull request!

### Questions?

If you have any questions or suggestions : schnaror@gmail.com

