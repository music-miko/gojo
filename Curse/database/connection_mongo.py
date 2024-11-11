import datetime

from Curse.database.dbname import dbname

connection = dbname.connection
chatu = dbname.chatu

first_found_date = datetime.datetime.now()


def connectDB(user_id, chat_id):
    connectionData = connection.find_one({"user_id": user_id})
    totalConnections = connection.count_documents({})
    NumofConnections = totalConnections + 1

    if connectionData is None:
        connection.insert_one(
            {
                "_id": NumofConnections,
                "user_id": user_id,
                "connection": True,
                "connected_chat": int(chat_id),
            }
        )
    else:
        connection.update_one(
            {"user_id": user_id},
            {"$set": {"connection": True, "connected_chat": int(chat_id)}},
            upsert=True,
        )


def GetConnectedChat(user_id):
    connectionData = connection.find_one({"user_id": user_id})
    if connectionData is not None:
        chat_id = connectionData["connected_chat"]
        return chat_id
    else:
        return None


def isChatConnected(user_id) -> bool:
    connectionData = connection.find_one({"user_id": user_id})
    if connectionData is not None:
        return connectionData["connection"]
    else:
        return False


def disconnectChat(user_id):
    connection.update_one({"user_id": user_id}, {"$set": {"connection": False}})


def reconnectChat(user_id):
    connection.update_one({"user_id": user_id}, {"$set": {"connection": True}})


def allow_collection(chat_id, chat_title, allow_collection):
    chat_data = chatu.find_one({"chat_id": chat_id})
    if chat_data == None:
        chatuNums = chatu.count_documents({})
        chatuIDs = chatuNums + 1

        ChatData = {
            "_id": chatuIDs,
            "chat_id": chat_id,
            "chat_title": chat_title,
            "first_found_date": first_found_date,
            "allow_collection": allow_collection,
        }

        chatu.insert_one(ChatData)
    else:
        chatu.update_one(
            {"chat_id": chat_id},
            {"$set": {"allow_collection": allow_collection}},
            upsert=True,
        )


def get_allow_connection(chat_id) -> bool:
    chat_data = chatu.find_one({"chat_id": chat_id})
    if chat_data is not None:
        if "allow_collection" in chat_data:
            return chat_data["allow_collection"]
        else:
            return False
    return False
