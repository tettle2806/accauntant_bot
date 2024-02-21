import os
import dotenv

dotenv.load_dotenv()

token = os.getenv('BOT_TOKEN')
admin_id = os.getenv('ADMIN_ID')
url = os.getenv('URL')
