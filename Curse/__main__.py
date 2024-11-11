import uvloop  # Comment it out if using on Windows
from Curse.bot_class import app

if __name__ == "__main__": 
    # uvloop.install()  # Comment it out if using on Windows
    app().run()
