from os import getcwd
from prettyconf import Configuration
from prettyconf.loaders import EnvFile, Environment

class SupportClass:
    def __init__(self, name):
        self.name = name

    def get_name(self):
        return self.name

env_file = f"{getcwd()}/.env"
config = Configuration(loaders=[Environment(), EnvFile(filename=env_file)])

class Config:
    """Config class for variables."""
    LOGGER = True
    BOT_TOKEN = config("BOT_TOKEN", default=None)
    API_ID = int(config("API_ID", default="123"))
    API_HASH = config("API_HASH", default=None)
    OWNER_ID = int(config("OWNER_ID", default=6965147961))
    MESSAGE_DUMP = int(config("MESSAGE_DUMP", default=-1001646232965))
    AuDD_API = config("AuDD_API", default=None)
    DEV_USERS = [
        int(i)
        for i in config(
            "DEV_USERS",
            default="6848223695",
        ).split(" ")
    ]
    SUDO_USERS = [
        int(i)
        for i in config(
            "SUDO_USERS",
            default="7185106962",
        ).split(" ")
    ]
    WHITELIST_USERS = [
        int(i)
        for i in config(
            "WHITELIST_USERS",
            default="7185106962",
        ).split(" ")
    ]
    GENIUS_API_TOKEN = config("GENIUS_API", default=None)
    RMBG_API = config("RMBG_API", default=None)
    DB_URI = config("DB_URI", default=None)
    DB_NAME = config("DB_NAME", default="Curse")
    BDB_URI = config("BDB_URI", default=None)
    NO_LOAD = config("NO_LOAD", default="").split()
    PREFIX_HANDLER = config("PREFIX_HANDLER", default="/").split()
    SUPPORT_GROUP = config("SUPPORT_GROUP", default="Lux_bot_support")
    SUPPORT_CHANNEL = config("SUPPORT_CHANNEL", default="Lux_bot_support")
    WORKERS = int(config("WORKERS", default=16))
    TIME_ZONE = config("TIME_ZONE", default='Asia/Kolkata')
    BOT_USERNAME = config("BOT_USERNAME", default=None)
    BOT_ID = config("BOT_ID", default=None)
    BOT_NAME = ""
    owner_username = "hunter_karan"

class Development:
    """Development class for variables."""
    LOGGER = True
    BOT_TOKEN = "5959061711:AAFvwYbdr5fI_kW3vajPcPQvjDAKQz3WT5I"
    API_ID = 9552179  # Your APP_ID from Telegram
    API_HASH = "fa6e0313afd8259094486d3256242102"  # Your APP_HASH from Telegram
    OWNER_ID = 6965147961  # Your telegram user id default to mine
    MESSAGE_DUMP = -1001646232965  # Your Private Group ID for logs
    DEV_USERS = ["1643851457", "6848223695"]
    SUDO_USERS = ["6848223695", "5458968679"]
    WHITELIST_USERS = ["7185106962"]
    DB_URI = "mongodb+srv://abdulrahaman001:databaseKomi@komi.mosqcfj.mongodb.net/?retryWrites=true&w=majority&appName=KOmi"  # Your mongo DB URI
    DB_NAME = "Curse"  # Your DB name
    NO_LOAD = []
    GENIUS_API_TOKEN = "gIgMyTXuwJoY9VCPNwKdb_RUOA_9mCMmRlbrrdODmNvcpslww_2RIbbWOB8YdBW9"
    RMBG_API = ""
    PREFIX_HANDLER = ["!", ".", "Komi ", "komi "]
    SUPPORT_GROUP = "Lux_bot_support"
    SUPPORT_CHANNEL = "Lux_bot_support"
    VERSION = "3.O"
    TIME_ZONE = 'Asia/Kolkata'
    BDB_URI = "mongodb+srv://safwandigi:Fazal2002@test.kzjdjnu.mongodb.net/?retryWrites=true&w=majority&appName=test"
    WORKERS = 8
    BOT_USERNAME = "Komi_RoXbot"
    BOT_ID = "5959061711"
    AuDD_API = ""
