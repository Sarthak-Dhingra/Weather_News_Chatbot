import gradio as gr
import requests
import datetime

# API keys
WEATHER_API_KEY = 'd29839d168e4ab7f249f0fc3b218473d'
NEWS_API_KEY = 'pub_49253885a874218dfbb1e180c675ce22396ae'

# Function to get weather information
def get_weather(location):
    try:
        # OpenWeatherMap API URL
        weather_url = f"http://api.openweathermap.org/data/2.5/weather?q={location}&appid={WEATHER_API_KEY}&units=metric"
        
        # Make a request to the OpenWeatherMap API
        weather_response = requests.get(weather_url)
        weather_data = weather_response.json()
        
        # Extract weather details
        if weather_response.status_code == 200:
            weather_main = weather_data['weather'][0]['main']
            weather_description = weather_data['weather'][0]['description']
            temperature = weather_data['main']['temp']
            humidity = weather_data['main']['humidity']
            wind_speed = weather_data['wind']['speed']
            city = weather_data['name']
            country = weather_data['sys']['country']

            weather_info = (
                f"**Weather in {city}, {country}:**\n"
                f"- Condition: {weather_main}, {weather_description.capitalize()}\n"
                f"- Temperature: {temperature}°C\n"
                f"- Humidity: {humidity}%\n"
                f"- Wind Speed: {wind_speed} m/s\n"
            )
        else:
            weather_info = "Sorry, I couldn't find the weather information for that location. Please try again."
        
    except Exception as e:
        weather_info = f"Error occurred while retrieving weather data: {str(e)}"
    
    return weather_info

# Function to get news headlines using Newsdata.io API
def get_news(category):
    try:
        # Newsdata.io API URL
        news_url = f"https://newsdata.io/api/1/news?apikey={NEWS_API_KEY}&country=us&category={category}"
        
        # Make a request to the Newsdata.io API
        news_response = requests.get(news_url)
        news_data = news_response.json()
        
        # Extract news details
        if news_response.status_code == 200:
            articles = news_data.get('results', [])
            if not articles:
                return "Sorry, I couldn't find any news articles for that category."

            news_info = "**Latest News Headlines:**\n"
            for article in articles[:5]:  # Limit to 5 articles
                title = article['title']
                description = article['description']
                url = article['link']
                news_info += f"- **{title}**\n  {description}\n  [Read more]({url})\n\n"
        
        else:
            news_info = "Sorry, I couldn't retrieve the news at this time. Please try again later."
        
    except Exception as e:
        news_info = f"Error occurred while retrieving news data: {str(e)}"
    
    return news_info

# Main function to get both weather and news
def get_weather_and_news(location, news_category):
    weather_info = get_weather(location)
    news_info = get_news(news_category)
    return weather_info, news_info

# Gradio Interface
demo = gr.Interface(
    fn=get_weather_and_news,
    inputs=[
        gr.Textbox(label="Enter location", placeholder="e.g. New York"),
        gr.Radio(label="Select News Category", choices=["general", "business", "entertainment", "health", "science", "sports", "technology"])
    ],
    outputs=[
        gr.Markdown(label="Weather Information"),
        gr.Markdown(label="News Headlines")
    ],
    title="Weather and News Chatbot",
    description="Enter a location to get the current weather and select a news category for the latest headlines."
)

demo.launch()

