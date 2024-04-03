import os
import dotenv

dotenv.load_dotenv()

token = os.getenv('BOT_TOKEN')
admin_id = os.getenv('ADMIN_ID')
url = os.getenv('URL')

type_of_review = ['😤Хочу пожаловатся 👎🏻',
                  '☹️Не понравилось, на 2 ⭐️⭐️',
                  '😐Удовлетворительно на 3 ⭐️⭐️⭐️',
                  '☺️Нормально, на 4 ⭐️⭐️⭐️⭐️',
                  '😊Все понравилось, на 5 ❤️']
