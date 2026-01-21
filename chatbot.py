import datetime, pyjokes, wikipedia, requests, ast, operator, re, os
from dotenv import load_dotenv

load_dotenv()

def get_date():
    today_date = datetime.date.today().strftime("%B %d,%Y")
    return f"Today's date is {today_date} "


def get_time():
    current_time = datetime.datetime.now().strftime("%I:%M:%p")
    return f"The current time is {current_time}" 

def tell_joke():
    joke = pyjokes.get_joke()
    return joke

def get_wikipedia_summary(query):
    try:
        summary = wikipedia.summary(query,sentences=2)
        return summary 
    except wikipedia.exceptions.DisambiguationError as e:
        return f"Your query is too broad. Try being more specific. For example: {e.options[:3]}"
    except wikipedia.exceptions.PageError:
        return "Sorry, I couldn't find any information on that topic."

def get_weather(city):
    api_key = os.getenv("WEATHER_API_KEY")
    base_url = "https://api.openweathermap.org/data/2.5/weather"
    params = {"q": city, "appid": api_key, "units": "metric"}

    try:
        response = requests.get(base_url,params = params)
        data = response.json()

        if data["cod"] == 200:
            main = data["main"]
            weather_desc = data["weather"][0]["description"]
            temp = main["temp"]
            humidity = main["humidity"]
            return f"The weather in {city} is {weather_desc} with a temperature of {temp}°C and humidity of {humidity}%."
        else:
            return f"Sorry I couldn't find the weather for {city}."
    except Exception as e:
        return "Sorry, I couldn't retrieve the weather right now."

def is_math_expression(text):
    text = text.lower()

    # Common math keywords or symbols
    keywords = ["plus", "minus", "times", "multiply", "divided", "divide", "+", "-", "*", "/", "power", "square root"]

    # Check if the sentence has any number or these keywords
    for word in keywords:
        if word in text:
            return True

    # If the user typed any digit, treat as math too
    if any(char.isdigit() for char in text):
        return True

    return False

def solve_math(user_input):
    text = user_input.lower()

    # Remove extra words that are not needed
    text = text.replace("what is", "")
    text = text.replace("calculate", "")
    text = text.replace("please", "")
    text = text.replace("?", "").strip()

    # Replace English words with symbols
    text = text.replace("plus", "+")
    text = text.replace("minus", "-")
    text = text.replace("times", "*")
    text = text.replace("multiplied by", "*")
    text = text.replace("divided by", "/")
    text = text.replace("divide by", "/")
    text = text.replace("divide", "/")
    text = text.replace("power", "**")

    try:
        # Evaluate the math expression
        result = eval(text)
        return f"The answer is {result}"
    except:
        return "Sorry, I couldn't calculate that. Please try something like 'what is 5 + 3'."


def chatbot_response(user_input):
    user_input = user_input.lower()
    if user_input == "bye":
        return "Goodbye! Have a nice day 😊"
    elif any(greet in user_input.split() for greet in ["hi", "hello", "hey"]):
        return "Hello there!"
    elif "how are you" in user_input:
        return "I’m doing great, thanks for asking!"
    elif "date" in user_input:
        return get_date()
    elif "time" in user_input:
        return get_time()
    elif "joke" in user_input or "jokes" in user_input:
        return tell_joke()
    elif ("what is" in user_input or "who is" in user_input or "tell me about" in user_input or "do you know about" in user_input) and "weather" not in user_input\
      and not is_math_expression(user_input):
        topic = user_input.replace("what is","").replace("who is","").replace("tell me about","").replace("do you know about","").strip()
        return get_wikipedia_summary(topic)
    elif "weather" in user_input:
        city = (
            user_input.replace("what is the weather in", "")
            .replace("what is the weather of", "")
            .replace("what is weather in", "")
            .replace("weather in", "")
            .replace("weather of", "")
            .replace("weather", "")
            .strip()
        )
        return get_weather(city)
    elif is_math_expression(user_input):
        return solve_math(user_input)

    else:
        return "I am not sure how to respond to that."

print("Hello! I am ChatBot.")
print("Type 'bye' to end the chat.")

while True:
    user_input = input("You: ")
    response = chatbot_response(user_input)
    print("ChatBot:", response)
    if user_input.lower() == "bye":
        break
