from Curse import DEV_USERS, OWNER_ID, SUDO_USERS, WHITELIST_USERS
from Curse.database.support_db import SUPPORTS

from Curse.vars import support_class
from some_modules.some_function import some_function 

# Initialize and use the support object
async def load_support_users():
    support = SupportClass()  # Initialize your support class here
    support_users = '1643851457' , '6848223695'  # Example data

    # Split the users and add them
    user_ids = support_users.split(',')
    for i in user_ids:
        i = i.strip()
        support.insert_support_user(int(i), "dev")  # Insert user with role "dev"
        support.insert_support_user(int(i),"sudo")
    for i in WHITELIST_USERS:
        
        support.insert_support_user(int(i),"whitelist")
    return

def get_support_staff(want = "all"):
    """
    dev, sudo, whitelist, dev_level, sudo_level, all
    """
    support = SUPPORTS()
    devs = support.get_particular_support("dev")
    sudo = support.get_particular_support("sudo")
    whitelist = support.get_particular_support("whitelist")

    if want in ["dev","dev_level"]:
        wanted = devs
    elif want == "sudo":
        wanted = sudo
    elif want == "whitelist":
        wanted = whitelist
    elif want == "sudo_level":
        wanted = sudo + devs
    else:
        wanted = list(set([int(OWNER_ID)] + devs + sudo + whitelist))

    return wanted
