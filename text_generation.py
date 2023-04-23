import requests
import json
from profanityfilter import ProfanityFilter
from textblob import TextBlob
import re
import asyncio

async def generate_text(chat, prompt, printing, timeout):
    # Check if chat is a boolean
    if not isinstance(chat, bool):
        raise ValueError("The 'chat' parameter must be a boolean.")

    # Check if printing is a boolean
    if not isinstance(printing, bool):
        raise ValueError("The 'printing' parameter must be a boolean.")

    # Check if prompt is a non-empty string
    if not isinstance(prompt, str) or not prompt.strip():
        raise ValueError("The 'prompt' parameter must be a non-empty string.")

    # Set the Chat variable
    Chat = chat

    api_key = "0000000000" # put api key here if wanted
    headers = {
        "apikey": api_key,
        "Client-Agent": "1:1",
        "Content-Type": "application/json"
    }

    # Get the list of available models and choose the fastest one
    models_url = "https://stablehorde.net/api/v2/status/models?type=text"
    models_response = requests.get(models_url, headers=headers)

    if models_response.status_code != 200:
        print(f"Error: {models_response.status_code}, {models_response.text}")
        exit(1)

    models = models_response.json()

    # Filter models based on the Chat variable
    if Chat:
        filtered_models = [model for model in models if "pygmalion" in model["name"]]
    else:
        filtered_models = [model for model in models if model["name"] != "Gustavosta/MagicPrompt-Stable-Diffusion" and all(substring not in model["name"] for substring in ["pygmalion", "Janeway", "Erebus", "Nerybus"])]

    # Function to prioritize models with a higher speed and a lower queue count
    def model_priority(model):
        speed = model["performance"]
        queue = model["queued"]
        priority = speed / (queue + 1)
        return priority, speed, queue

    # Choose the model with the highest priority
    best_model = max(filtered_models, key=model_priority)
    model_name = best_model["name"]
    priority, speed, queue = model_priority(best_model)

    # Initiate the asynchronous text generation request
    url = "https://stablehorde.net/api/v2/generate/text/async"
    payload = {
        "prompt": prompt,
        "params": {
            "n": 1,
            "max_length": 512,
            "singleline": False,
            "temperature": 0.5,
            "rep_pen": 1.1,
            "rep_pen_range": 1024,
            "rep_pen_slope": 0.7,
        },
        "models": [model_name],
        "trusted_workers": True,
        "slow_workers": True
    }

    # Print and alert user of stuff
    if printing:
        print(f"Fastest available model: {model_name}, Speed: {speed}, Queue: {queue}")
        print("Prompt:\n" + payload["prompt"])
        print("---")
        print("Sending request...")
        print("---")

    response = requests.post(url, headers=headers, data=json.dumps(payload))

    if response.status_code == 202:
        generation_id = response.json()["id"]
        if printing:
            print(f"Generation ID: {generation_id}")
    else:
        print(f"Error: {response.status_code}, {response.text}")
        exit(1)

    # Create an instance of ProfanityFilter
    pf = ProfanityFilter()

    # Function to check if the text contains profanity
    def contains_profanity(text):
        return pf.is_profane(text)

    def is_negative(text, threshold=0.0):
        blob = TextBlob(text)
        sentiment = blob.sentiment.polarity
        return sentiment < threshold, sentiment

    # Keep checking the status until it's complete or times out
    status_url = f"https://stablehorde.net/api/v2/generate/text/status/{generation_id}"
    start_time = asyncio.get_event_loop().time()
    while True:
        current_time = asyncio.get_event_loop().time()
        if printing:
          print(timeout)
          print(current_time - start_time)
        if current_time - start_time > timeout:
            if printing:
                print("Timeout reached.")
            return "Timeout: generation took too long", True

        status_response = requests.get(status_url, headers=headers)
        status = status_response.json()

        if status_response.status_code == 200:
            if status["done"]:
                # Retrieve the generated text from the first completed generation
                for generation in status["generations"]:
                    if generation["state"] == "ok":
                        text = generation['text']
                        # Remove special characters and spaces to aid profanity filter
                        cleaned_text = re.sub(r'[^\w\s]+', '', text)
                        if printing:
                            print(cleaned_text)
                        if not contains_profanity(cleaned_text):
                            negative, sentiment = is_negative(cleaned_text)
                            if printing:
                              print("Negative:", negative)
                              print("Sentiment:", sentiment)
                            if not negative or sentiment >= -0.6:
                                if printing:
                                    print(f"Generated text: {text}")
                                return text, False
                            else:
                                if printing:
                                    print("Inappropriate content detected.")
                                return "The AI's response contained inappropriate content. Please rephrase your input.", True
                        else:
                            if printing:
                                print("Inappropriate content detected.")
                            return "The AI's response contained inappropriate content. Please rephrase your input.", True
                break
            else:
                if printing:
                    print("Status: still processing")
        else:
            if printing:
                print(f"Error: {status_response.status_code}, {status_response.text}")
            break

        await asyncio.sleep(1)  # Wait for 1 second before checking again
