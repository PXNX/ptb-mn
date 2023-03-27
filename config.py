import os

from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('TELEGRAM')
DATABASE_URL = os.getenv("DATABASE_URL")  # .replace("postgres", "postgresql", 1)
DATABASE_URL_NN = os.getenv("DATABASE_URL_NN")
TEST_MODE = os.getenv("TESTING", False)
PORT = int(os.getenv("PORT", 8080))

CHANNEL_MEME = -1001486678205
CHANNEL_SOURCE = -1001372304339

LOG_GROUP = -1001739784948

NYX = 703453307
ADMINS = (
    NYX,
    525147382,  # Melik
    466451473,  # Maxe
    5945157782  # MN-Kontakt
)

BINGO_ADMINS = ADMINS + (
    1869587716,  # TheObserver
    298169115  # Michael Kohl
)

# Constants
PLACEHOLDER = "║"
