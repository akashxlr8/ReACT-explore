# AI Agents Demonstration

![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![GitHub Workflow Status](https://img.shields.io/github/actions/workflow/status/yourusername/ai-agents-demonstration/ci.yml?branch=main)
![GitHub Last Commit](https://img.shields.io/github/last-commit/yourusername/ai-agents-demonstration)

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [How It Works](#how-it-works)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
  - [Basic Usage](#basic-usage)
  - [Enable Verbose Logging](#enable-verbose-logging)
- [Available Actions](#available-actions)
  - [Wikipedia](#wikipedia)
  - [Weather](#weather)
  - [Country Info](#country-info)
- [Logging](#logging)
  - [Controlling Logging via Environment Variables](#controlling-logging-via-environment-variables)
  - [Fine-Grained Control for Specific Loggers](#fine-grained-control-for-specific-loggers)
- [Examples](#examples)
  - [Example 1: Fetching Country Information and Weather](#example-1-fetching-country-information-and-weather)
  - [Example 2: Getting Current Weather](#example-2-getting-current-weather)
- [Screenshots](#screenshots)
- [Contributing](#contributing)
- [Support](#support)
- [License](#license)

## Introduction

**AI Agents Demonstration** is a Python script that showcases how AI agents can interact with various APIs to perform specific actions based on user input. Leveraging the power of `litellm`, `httpx`, and `BeautifulSoup`, this script demonstrates how AI can intelligently decide which actions to execute to provide accurate and relevant information to users.

## Features

- **Dynamic Action Selection:** AI agents choose the most appropriate actions (e.g., fetching Wikipedia summaries, weather information, or country details) based on user queries.
- **API Integration:** Integrates with Wikipedia API, OpenWeatherMap API, and REST Countries API to retrieve real-time data.
- **Robust Error Handling:** Implements decorators to handle exceptions gracefully during API calls.
- **Configurable Logging:** Allows users to control the verbosity of logs, enabling detailed logging only when needed.
- **Conversation History Management:** Maintains and resets conversation history to ensure fresh interactions.
- **Modular Design:** Easy to extend with additional actions or integrate into larger projects.

## How It Works

The AI agent processes user input to determine the intent and necessary actions. It utilizes the `litellm` library to handle AI-driven decision-making, selecting the appropriate API to call based on the context of the query. The responses from these APIs are then formatted and presented to the user in a coherent manner.

## Prerequisites

- Python 3.8 or higher
- [pip](https://pip.pypa.io/en/stable/installation/)

## Installation

1. **Clone the Repository**

   ```bash
   git clone https://github.com/yourusername/ai-agents-demonstration.git
   cd ai-agents-demonstration
   ```

2. **Create a Virtual Environment (Optional but Recommended)**

   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**

   ```bash
   pip install -r requirements.txt
   ```

   **`requirements.txt`:**

   ```plaintext
   litellm
   httpx
   beautifulsoup4
   python-dotenv
   ```

## Configuration

The script relies on several environment variables to function correctly. Create a `.env` file in the project root or set the variables in your environment.

### Required Environment Variables

- `GROQ_API_KEY`: Your API key for the Groq provider used by `litellm`.
- `OPENWEATHER_API_KEY`: Your OpenWeatherMap API key for fetching weather data.

### Optional Environment Variables

- `LOG_LEVEL`: Sets the logging level. Defaults to `WARNING`. Set to `INFO` to enable detailed logs.

**Example `.env` File:**

```dotenv
GROQ_API_KEY=your_groq_api_key
OPENWEATHER_API_KEY=your_openweather_api_key
LOG_LEVEL=WARNING
```

**Load Environment Variables:**

You can use the `python-dotenv` package to load variables from a `.env` file. This is already handled in the `app.py`.

```python:app.py
from dotenv import load_dotenv
load_dotenv()
```

## Usage

Run the `app.py` script to start the AI agent interaction.

```bash
python app.py
```

### Basic Usage

Upon running the script, you will be prompted to enter your query. The AI agent will process your input and execute the necessary actions to provide a response.

**Example:**

```
Enter your query: What is the weather in Paris and tell me about its history.
```

### Enable Verbose Logging

To enable detailed logging, set the `LOG_LEVEL` environment variable to `INFO` or use the `--verbose` flag if implemented.

**Using Environment Variables:**

```bash
export LOG_LEVEL=INFO
python app.py
```

**Using Command-Line Argument:**

```bash
python app.py --verbose
```

## Available Actions

### Wikipedia

Fetches a summary from Wikipedia based on the user's query.

- **Function:** `wikipedia(q)`
- **Parameters:**
  - `q` (str): The search query for Wikipedia.
- **Returns:** A cleaned summary string.

### Weather

Retrieves current weather information for a specified city.

- **Function:** `get_weather(city)`
- **Parameters:**
  - `city` (str): The name of the city to fetch weather data for.
- **Returns:** A string describing the current weather and temperature.

### Country Info

Provides specific details about a country, including its capital, population, and languages.

- **Function:** `get_country_info(country_name)`
- **Parameters:**
  - `country_name` (str): The name of the country to retrieve information about.
- **Returns:** A string containing the country's capital, population, and languages.

## Logging

The application uses Python's `logging` module to provide informative logs. By default, the logging level is set to `WARNING`. To view detailed logs, set the `LOG_LEVEL` to `INFO`.

### Controlling Logging via Environment Variables

Set the `LOG_LEVEL` environment variable to control the verbosity.

```bash
export LOG_LEVEL=INFO  # Enables INFO level logs
export LOG_LEVEL=WARNING  # Enables WARNING and above
```

### Fine-Grained Control for Specific Loggers

You can customize logging for specific modules within the script by modifying the logging configuration in `app.py`.

```python:app.py
# Configure specific loggers if needed
if args.verbose:
    logging.getLogger('LiteLLM').setLevel(logging.INFO)
    logging.getLogger('httpx').setLevel(logging.INFO)
```

## Examples

### Example 1: Fetching Country Information and Weather

**User Query:**

```
Summarize information about France and tell me the weather in its capital.
```

**Bot Actions:**

- Action: `country_info: France`
- Action: `weather: Paris`

**Final Response:**

```
France: Capital is Paris, Population: 67391582, Languages: French
The current weather in Paris is clear sky with a temperature of 25°C.
```

### Example 2: Getting Current Weather

**User Query:**

```
What is the current weather in Tokyo?
```

**Bot Actions:**

- Action: `weather: Tokyo`

**Final Response:**

```
The current weather in Tokyo is light rain with a temperature of 18°C.
```

## Screenshots

### Running the AI Agent

![AI Agent Running](screenshots/agent_running.png)

### Example Interaction

![AI Agent Interaction](screenshots/interaction_example.png)

*Note: Replace the image URLs with actual screenshots placed in the `screenshots` directory.*

## Contributing

Contributions are welcome! Please follow these steps to contribute:

1. **Fork the Repository**

2. **Create a New Branch**

   ```bash
   git checkout -b feature/YourFeature
   ```

3. **Commit Your Changes**

   ```bash
   git commit -m "Add YourFeature"
   ```

4. **Push to the Branch**

   ```bash
   git push origin feature/YourFeature
   ```

5. **Open a Pull Request**

Please ensure your code adheres to the existing style and includes necessary tests.

### Development Guidelines

- Follow [PEP 8](https://pep8.org/) style guidelines.
- Write clear and concise commit messages.
- Include tests for new features or bug fixes.
- Update the documentation as necessary.

## Support

If you encounter any issues or have questions, please open an [issue](https://github.com/yourusername/ai-agents-demonstration/issues) on GitHub or contact [youremail@example.com](mailto:youremail@example.com).

## License

This project is licensed under the [MIT License](LICENSE).

---