# RouteLLM: The Ultimate AI Matchmaker 🚀

Ever wondered what happens when Claude Sonnet 3.5, OpenAI o1, GPT-4o, and Gemini walk into a bar? 🍻 Well, welcome to **RouteLLM**—where AI egos clash and only the smartest survive!

## 🧐 What is RouteLLM?

RouteLLM is an innovative application designed to be the ultimate AI matchmaker! Imagine speed dating for AI models, but with a twist of neural networks and zero awkward silences. 🤖✨ Watch as our brainy bots battle it out in a high-stakes showdown, where the best model gets picked to answer your queries.

### Key Features:

1. **Custom Scoring System**: Based on response time, fluency, and humor.
2. **Parallel Execution**: API requests will be made in parallel using asynchronous programming.
3. **User Interface (UI)**: Django and Bootstrap 5 will be used for the front-end.
4. **Fluency Analysis**: Use NLP libraries like spacy or transformers to check for grammar and coherence in the responses.
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

## How it works:

1. TextBlob Sentiment returns a polarity value between -1 (negative) and 1 (positive).
2. VADER Sentiment also provides a compound score on the same scale.
3. We average the sentiment scores from both libraries to get a combined sentiment score.

## ⚙️ Installation

To get started with RouteLLM, follow these steps:

### Prerequisites
- Python 3.8 or higher
- Git

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/RouteLLM.git
   cd RouteLLM
