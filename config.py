from dotenv import load_dotenv
from os import getenv

load_dotenv()

BOT_TOKEN = getenv("TOKEN")

user_money = 5000

admin_ids = [getenv("ADMIN_ID"), getenv("ADMIN_ID2"), getenv("ADMIN_ID3")]

DB_FILE1 = "user_database.db"

DB_FILE2 = "shop.db"

symbols = [
    '💎', '🍀', '🔔', '🍊', '🍇', '🌟', '🎰', '🍒', '🔔', '🔔', '🔔', '🔔', '🔔', '🔔', '🔔', '🔔', '🔔', '🌟', '🌟', '🌟', '🌟', '🌟', '🌟',
    '🌟', '🌟', '🌟', '🌟', '🌟', '🌟', '🍒', '🍒', '🍒', '🍒', '🍒', '💎', '💎', '💎', '💎', '💎', '💎', '💎', '💎', '💎', '💎', '💎', '💎',
    '🍇', '🍇', '🍇', '🍇', '🔔', '🍊', '🍀', '🍀', '🍀', '🍀', '🍀', '🍀', '🍀', '🍀', '🍊', '🍊', '🍊', '🍊', '🍊', '🍊', '🍊', '🍊', '🍊', '🍊', '🍊',
    '🔔', '🍊', '🍀', '🔔', '🍊', '🍀', '🔔', '🍊', '🎰', '🎰', '🎰', '🎰', '🍒', '🍒', '🍒', '🍒', '🍒', '🍒', '🍒', '💎', '💎', '💎', '🍒', '🍒', '🍒',
]
