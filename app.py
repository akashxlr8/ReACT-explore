import litellm
import os
import re
import httpx
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)

def api_call_handler(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            error_msg = f"An error occurred in {func.__name__}: {str(e)}"
            print(error_msg)
            return error_msg
    return wrapper

@api_call_handler
def wikipedia(q):
    response = httpx.get("https://en.wikipedia.org/w/api.php", params={
        "action": "query",
        "list": "search",
        "srsearch": q,
        "format": "json"
    })
    response.raise_for_status()
    if response.json()["query"]["search"]:
        snippet = response.json()["query"]["search"][0]["snippet"]
        print(f"\nWikipedia API Response: {snippet}")
        return snippet
    else:
        no_results = "No Wikipedia results found."
        print(no_results)
        return no_results

@api_call_handler
def get_country_info(country_name):
    url = f"https://restcountries.com/v3.1/name/{country_name}"
    response = httpx.get(url)
    response.raise_for_status()
    data = response.json()
    if data:
        country = data[0]
        capital = country.get('capital', ['N/A'])[0]
        population = country.get('population', 'N/A')
        languages = ', '.join([lang for lang in country.get('languages', {}).values()]) if country.get('languages') else 'N/A'
        result = f"{country_name}: Capital is {capital}, Population: {population}, Languages: {languages}"
        print(f"\nCountry Info API Response: {result}")
        return result
    else:
        no_info_msg = f"No information found for {country_name}"
        print(no_info_msg)
        return no_info_msg

@api_call_handler
def get_weather(city):
    api_key = os.getenv("OPENWEATHER_API_KEY")  # Fetch from environment variables
    if not api_key:
        error_msg = "Weather API key not found. Please set the OPENWEATHER_API_KEY environment variable."
        print(error_msg)
        return error_msg
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    response = httpx.get(url)
    print(f"\nWeather API Status Code: {response.status_code}")  # Debug print
    
    if response.status_code == 200:
        data = response.json()
        weather = data['weather'][0]['description']
        temp = data['main']['temp']
        result = f"The current weather in {city} is {weather} with a temperature of {temp}°C."
        
        # Make this stand out in the console
        print("\n" + "="*80)
        print(result)
        print("="*80 + "\n")
        
        return result
    else:
        error_msg = f"Failed to retrieve weather data: HTTP {response.status_code}"
        print(error_msg)  # Debug print
        return error_msg

known_actions = {
    "wikipedia": wikipedia,
    "weather": get_weather,
    "country_info": get_country_info
}

class GPTBot:
    def __init__(self, system=""):
        self.system = system
        self.history = []  # Store the full conversation history

    def __call__(self, message):
        # Clear history for each new query to start fresh
        self.history = []
        
        if self.system:
            self.history.append({"role": "system", "content": self.system})

        self.history.append({"role": "user", "content": message})
        return self.execute()

    def execute(self):
        try:
            # Replace OpenAI with LiteLLM call
            completion = litellm.completion(
                model="groq/mixtral-8x7b-32768", 
                messages=self.history,
                api_key=os.getenv("GROQ_API_KEY")  # Ensure this environment variable is set
            )
            response = completion.choices[0].message.content
            self.history.append({"role": "assistant", "content": response})
            return response
        except Exception as e:
            logging.error("Error during API call: %s", e)
            return "Sorry, I encountered an error."

    def reset(self):
        # Reset the conversation history
        self.history = []

prompt = """
You are a sophisticated chatbot that MUST use the available actions to answer questions. Depending on the user's query, you should select the most appropriate action to retrieve accurate and relevant information.

Available actions:
- wikipedia: Fetches a summary from Wikipedia. Use this for comprehensive overviews or detailed descriptions.
- weather: Retrieves current weather information. Use this for any temperature or weather-related queries.
- country_info: Provides specific details about a country, including its capital, population, and languages.

IMPORTANT:
- You MUST use EXACTLY this format on a single line for actions:
  Action: action_name: parameter

- Select the most appropriate action(s) based on the user's question.
- DO NOT include numbers, thinking steps, or any other text in the action line.
- WAIT for the observation after each action before proceeding.
- DO NOT make up or guess any data - only use the data provided by the actions.

Example scenarios:

1. For a query like "What is the population of Germany and its current weather?":
   - Action: country_info: Germany
   - Action: weather: Berlin

2. For a query like "Tell me about the history of Germany and its current weather.":
   - Action: wikipedia: "History of Germany"
   - Action: weather: Berlin

3. **For a query like "What is the current weather in Tokyo?":**
   - Action: weather: Tokyo

After receiving observations, provide a natural response using the retrieved data.
""".strip()

# Updated regex to handle optional numbering
action_re = re.compile(r'^(?:\d+\.\s+)?Action:\s*(\w+):\s*(.+)$')

def query(bot, question, max_turns=10):
    i = 0
    next_prompt = question
    final_response = ""
    print("\nInitial Question:", question)

    while i < max_turns:
        i += 1
        try:
            result = bot(next_prompt)
            print(f"\nTurn {i}:")
            print("Bot's Raw Response:", result)

            # Initialize to check if any action was executed in this turn
            actions_executed = []

            # Iterate through each line to find actions
            for line in result.split('\n'):
                match = action_re.match(line.strip())
                if match:
                    action, action_input = match.groups()
                    print(f"\nExecuting Action: {action} with input: {action_input}")
                    if action in known_actions:
                        observation = known_actions[action](action_input)
                        next_prompt = f"Observation: {observation}"
                        print(f"Action Result: {observation}")
                        actions_executed.append(action)
            
            if not actions_executed:
                # No action found; assume final response
                final_response = result
                print("\nNo more actions detected, ending conversation.")
                break

        except Exception as e:
            print("An error occurred:", str(e))
            break

    return final_response

def main():
    bot = GPTBot(prompt)
    
    # List of test questions
    questions = [
        # "Use the weather action to tell me the current temperature in Mumbai",
        "What is the weather in the capital of India?",
        # "Provide the population of Germany and the current weather in its capital.",
        # "Summarize information about France and tell me the weather in its capital."
    ]
    
    for question in questions:
        print("\n-----------------------------------Starting conversation...-----------------------------------")
        response = query(bot, question)
        print("\nFinal Response:", response)
        bot.reset()

if __name__ == "__main__":
    main()