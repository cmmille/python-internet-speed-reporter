import InternetSpeedTwitterBot
import dotenv, os

dotenv.load_dotenv()
username = os.getenv("username")
password = os.getenv("password")

speed_bot = InternetSpeedTwitterBot.InternetSpeedTwitterBot()
speed_bot.get_internet_speed()
speed_bot.tweet_at_provider(username, password, 400)