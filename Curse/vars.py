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
    OWNER_ID = int(config("OWNER_ID", default=6848223695))
    MESSAGE_DUMP = int(config("MESSAGE_DUMP", default=-1002324687097))
    AuDD_API = config("AuDD_API", default=None)
    DEV_USERS = [
        int(i)
        for i in config(
            "DEV_USERS",
            default="7186437295",
        ).split(" ")
    ]
    SUDO_USERS = [
        int(i)
        for i in config(
            "SUDO_USERS",
            default="6606591031",
        ).split(" ")
    ]
    WHITELIST_USERS = [
        int(i)
        for i in config(
            "WHITELIST_USERS",
            default="6309921371",
        ).split(" ")
    ]
    GENIUS_API_TOKEN = config("GENIUS_API", default=None)
    RMBG_API = config("RMBG_API", default=None)
    DB_URI = config("DB_URI", default=None)
    DB_NAME = config("DB_NAME", default="Curse")
    BDB_URI = config("BDB_URI", default=None)
    NO_LOAD = config("NO_LOAD", default="").split()
    PREFIX_HANDLER = config("PREFIX_HANDLER", default="/").split()
    SUPPORT_GROUP = config("SUPPORT_GROUP", default="nothing_bots_support")
    SUPPORT_CHANNEL = config("SUPPORT_CHANNEL", default="The_hogwart")
    WORKERS = int(config("WORKERS", default=16))
    TIME_ZONE = config("TIME_ZONE", default='Asia/Kolkata')
    BOT_USERNAME = config("BOT_USERNAME", default=None)
    BOT_ID = config("BOT_ID", default=None)
    BOT_NAME = "ʜᴀʀʀʏメᴘᴏᴛᴛᴇʀ"
    owner_username = "its_damiann"

class Development:
    """Development class for variables."""
    LOGGER = True
    BOT_TOKEN = "7858576961:AAHGQrUExMVK5eEIDIRWVm2ZRHH7DVFJBOg"
    API_ID = 9552179  # Your APP_ID from Telegram
    API_HASH = "fa6e0313afd8259094486d3256242102"  # Your APP_HASH from Telegram
    OWNER_ID = 6848223695  # Your telegram user id default to mine
    MESSAGE_DUMP = -1002023182491  # Your Private Group ID for logs
    DEV_USERS = ["7186437295", " 6606591031"]
    SUDO_USERS = ["5350261891", "6557496294", "6309921371", "6965147961"]
    WHITELIST_USERS = ["5692379500"]
    DB_URI = "mongodb+srv://sakibsk304:HKswQwkHU5mGlAUv@cluster0.w8xnr.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"  # Your mongo DB URI
    DB_NAME = "Cluster0"  # Your DB name
    NO_LOAD = []
    GENIUS_API_TOKEN = "gIgMyTXuwJoY9VCPNwKdb_RUOA_9mCMmRlbrrdODmNvcpslww_2RIbbWOB8YdBW9"
    RMBG_API = ""
    PREFIX_HANDLER = ["!", ".", "harry ", "harry ", "/"]
    SUPPORT_GROUP = "Harry_PotterxSupport"
    SUPPORT_CHANNEL = "Hogwarts_updates"
    VERSION = "3.O"
    TIME_ZONE = 'Asia/Kolkata'
    BDB_URI = "mongodb+srv://orewauzumaki:orewauzumaki@cluster0.bmhengh.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
    WORKERS = 8
    BOT_USERNAME = "Harry_RoxBot"
    BOT_ID = "7858576961"
    AuDD_API = ""
