import discord
import os
import pymongo
from pymongo import MongoClient

from dotenv import load_dotenv

cluster = MongoClient("XXXX")
db = cluster["SharkGang"]
collection = db["Counts"]

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

client = discord.Client()

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith("-"):
        thing_to_update = message.content.split("-")[1]
        thing_to_update = thing_to_update.lower()
        myquery = {"item":thing_to_update}
        if (collection.count_documents(myquery) == 0):
            await message.channel.send(f"SharkBird has never defeated {thing_to_update}, its count cannot be reduced.")
        else:
            query = {"item":thing_to_update}
            item = collection.find(query)
            for result in item:
                value = result["value"]
            if value > 0:
                value = value - 1
            else:
                value = 0
                await message.channel.send(f"SharkBird has never defeated {thing_to_update}, its count is already zero")
            collection.update_one({"item":thing_to_update}, {"$set":{"value":value}})

    if message.content.startswith("+count"):
        count_check = message.content.split(" ", 1)
        if len(count_check) == 1:
            cursor = collection.find({})
            total_value = 0
            for document in cursor:
                value = document["value"]
                total_value += value
            await message.channel.send(f"SharkBird has defeated {total_value} enemies.")
        elif len(count_check) == 2:
            myquery = {"item": count_check[1]}
            item = collection.find(myquery)
            if (collection.count_documents(myquery) == 0):
                await message.channel.send(f"SharkBird has never defeated {count_check[1]}.")
            else:
                value = ""
                for result in item:
                    value = result["value"]
                await message.channel.send(f"SharkBird has defeated {count_check[1]} {value} times.")

    elif message.content.startswith("+"):
        thing_to_update = message.content.split("+")[1]
        thing_to_update = thing_to_update.split(" ")
        num_of_things = 1
        if len(thing_to_update) == 2:
            num_of_things = int(thing_to_update[1])
        thing_to_update = thing_to_update[0].lower()
        print(thing_to_update, num_of_things)

        myquery = {"item":thing_to_update}
        if (collection.count_documents(myquery) == 0):
            post = {"item":thing_to_update, "value": 1}
            collection.insert_one(post)
        else:
            query = {"item":thing_to_update}
            item = collection.find(query)
            for result in item:
                value = result["value"]
            value = value + num_of_things
            collection.update_one({"item":thing_to_update}, {"$set":{"value":value}})

client.run(TOKEN)
