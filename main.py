import os
from pyrogram import Client, filters
import requests

bot = Client(
    "movie_bot",
    api_id=int(os.environ["API_ID"]),
    api_hash=os.environ["API_HASH"],
    bot_token=os.environ["BOT_TOKEN"]
)

# API Endpoints
MOVIE_SEARCH_API_URL = "https://www.dark-yasiya-api.site/movie/sinhalasub/search"
DETAILS_API_URL = "https://www.dark-yasiya-api.site/movie/sinhalasub/movie"

# Variable to store search results
movie_results = []

# Search Movie Function
def search_movie(movie_name):
    try:
        response = requests.get(MOVIE_SEARCH_API_URL, params={"text": movie_name})
        if response.status_code == 200:
            movies = response.json().get("result", {}).get("data", [])
            if movies:
                global movie_results
                movie_results = movies  # Save the search results globally
                results = []
                for idx, movie in enumerate(movies, start=1):
                    title = movie.get("title", "No Title")
                    year = movie.get("year", "Unknown Year")
                    imdb = movie.get("imdb", "No Rating")
                    results.append(f"<b>{idx}. 🏷 Title ➜ {title}\n🗓 Year ➜ {year}\n⭐️ IMDB ➜ {imdb}\n</b>")
                return "\n".join(results)
            else:
                return "<b>⚠️ සමාවන්න, මූවී හමු නොවුණා!</b>"
        else:
            return f"⚠️<b> බොට්ගේ ගැටලුවකි: {response.status_code}</b>"
    except Exception as e:
        return f"⚠️ <b>දෝෂයකි: {str(e)}</b>"

# Get Movie Details Function
def get_movie_details(movie_url):
    try:
        response = requests.get(DETAILS_API_URL, params={"url": movie_url})
        if response.status_code == 200:
            data = response.json().get("result", {}).get("data", {})
            title = data.get("title", "No Title")
            year = data.get("date", "Unknown Year")
            country = data.get("country", "Unknown Country")
            runtime = data.get("runtime", "Unknown Runtime")
            imdb_rate = data.get("imdbRate", "No Rating")
            description = data.get("description", "No Description")
            author = data.get("subtitle_author", "Unknown person")
            director = data.get("director", "Unknown director")
            category = data.get("category", "No Categories")
            dl_links = data.get("dl_links", "no links")

            # Return formatted details (excluding download links and poster)
            return (f"<b>🏷 Title ➜ {title}</b>\n\n"
                    f"🗓 <b>Year ➜ {year}</b>\n"
                    f"🌍 <b>Country ➜ {country}</b>\n"
                    f"⏰ <b>Runtime ➜ {runtime}</b>\n"
                    f"⭐️ <b>IMDB Rating ➜ {imdb_rate}</b>\n"
                    f"🎥 <b>Director ➜ {director}</b>\n"
                    f"✍🏻 <b>Subtitled By ➜ {author}</b>\n\n"
                    f"📖 <b>Description ➜ \n{description}</b>")
        else:
            return f"<b>⚠️ API ගැටලුවකි: {response.status_code}</b>"
    except Exception as e:
        return f"<b>⚠️ දෝෂයකි: {str(e)}</b>"

# Start Command Handler
@bot.on_message(filters.command("start") & filters.private)
def start_command(bot, message):
    bot.send_message(
        message.chat.id,
        "👋<b> හෙලෝ!\n\nමට මූවී එකක නමක් එවන්න. මම ඒ ගැන විස්තර ලබා දෙන්නම්.</b>"
    )

# Movie Search Command Handler
@bot.on_message(filters.private & ~filters.command("start"))
def search_movies_command(bot, message):
    user_input = message.text.strip()
    
    # If user sends a number, return details of the corresponding movie
    if user_input.isdigit():
        index = int(user_input) - 1
        if 0 <= index < len(movie_results):
            movie_url = movie_results[index]["link"]
            bot.send_message(message.chat.id, "<b>සොයමින්...</b>")
            details = get_movie_details(movie_url)
            bot.send_message(message.chat.id, details)
        else:
            bot.send_message(message.chat.id, "<b>⚠️ වැරදි අංකයක් ලබාදී ඇත!</b>")
    else:
        # Else, treat the input as a movie name
        bot.send_message(message.chat.id, "🔍<b>සොයමින්\n<i>මදක් රැදී සිටින්න...</i></b>")
        result = search_movie(user_input)
        bot.send_message(message.chat.id, result)

# Start Bot
print("Bot is running...")
bot.run()
