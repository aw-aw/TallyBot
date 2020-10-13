import discord
import os
import pymongo
from pymongo import MongoClient

from dotenv import load_dotenv

# +1 yarok
# -1 yuriko
# +count
# +count yarok
# +items

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

cluster = MongoClient(os.getenv('MONGO_DB_URL'))
db = cluster["SharkGang"]
collection = db["Counts"]

client = discord.Client()

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.split(" ")[0] == "-" or message.content.split(" ")[0] == "+":
        await message.channel.send("Oops, you added an extra space. Please resend your message.")

    if message.content.startswith("-"):
        fork = message.content.split("-", 1)
        fork = fork[1].split(" ", 1)
        item_decreased = fork[0]
        myquery = {"item":item_decreased}
        if (collection.count_documents(myquery) == 0):
            await message.channel.send(f"SharkBird has never defeated {item_decreased}.")
        else:
            item = collection.find(myquery)
            for result in item:
                value = result["value"]
            value -= 1
            if value < 0:
                value = 0
            if value == 0:
                collection.delete_one(myquery)
            else:
                collection.update_one({"item":item_decreased}, {"$set":{"value":value}})

    if message.content.startswith("+"):
        fork = message.content.split("+", 1)
        fork = fork[1].split(" ", 1)
        if fork[0] == "count":
            if len(fork) == 1:
                cursor = collection.find({})
                total_value = 0
                for document in cursor:
                    value = document["value"]
                    total_value += value
                if total_value == 1:
                    await message.channel.send(f"SharkBird has defeated {total_value} enemy.")
                else:
                    await message.channel.send(f"SharkBird has defeated {total_value} enemies.")
            else:
                myquery = {"item": fork[1].lower()}
                item = collection.find(myquery)
                if (collection.count_documents(myquery) == 0):
                    await message.channel.send(f"SharkBird has never defeated {fork[1]}.")
                else:
                    value = ""
                    for result in item:
                        value = result["value"]
                    if value == 1:
                        await message.channel.send(f"SharkBird has defeated {fork[1]} {value} time.")
                    else:
                        await message.channel.send(f"SharkBird has defeated {fork[1]} {value} times.")
        elif fork[0] == "items":
            cursor = collection.find({})
            output_message = "SharkrBird has defeated the following commanders:\n"
            for document in cursor:
                item = document["item"]
                value = document["value"]
                output_message += str(value)
                output_message += " "
                output_message += str(item)
                output_message += "\n"
            await message.channel.send(output_message)
        else:
            increase = int(fork[0])
            item_increased = fork[1]
            myquery = {"item":item_increased}
            if (collection.count_documents(myquery) == 0):
                post = {"item":item_increased, "value": increase}
                collection.insert_one(post)
            else:
                item = collection.find(myquery)
                for result in item:
                    value = result["value"]
                value = value + increase
                collection.update_one({"item":item_increased}, {"$set":{"value":value}})

client.run(TOKEN)
