from discord.ext import commands
import discord
# the ai shit
import aiohttp
import json
import time
import asyncio

import random
import os
import json
from datetime import datetime
import pytz

# tts ai... might need multi accs..
#import tts

bot = commands.Bot(command_prefix='.')


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')
    print()

async def LocalUwuifyStream(messages, dmessage, ogmessage):
    currenttime = datetime.now(pytz.timezone('Europe/Stockholm')).strftime("%Y-%m-%d %H:%M")
    url = "http://localhost:11434/api/chat"
    payload = {
        "model": "benevolentjoker/nsfwvanessa:latest",
        "stream": True,
        "messages": [{"role": "system", "content": f"Current Date And Time is: {currenttime} in Swedish time format. Always respond with this time format. Do not use previous messages to retrieve time.",}] + messages + [{"role": "user", "content": ogmessage.content}]
    }
    accumulated_content = ""
    edit_count = 0
    edit_threshold = 7
    
    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=payload) as response:
            async for line in response.content:
                if line:
                    json_line = line.decode('utf-8')
                    data = json.loads(json_line)
                    content = data.get("message", {}).get("content", "")
                    
                    accumulated_content += content
                    edit_count += 1

                    if edit_count >= edit_threshold:
                        await dmessage.edit(content=accumulated_content)
                        edit_count = 0
                        await asyncio.sleep(0)
                
            if accumulated_content:
                await dmessage.edit(content=f"<@{ogmessage.author.id}>\n{accumulated_content}")
    
    return accumulated_content

responses = [
    "Sprinkling magic on it~!",
    "Hold on, adding extra cuteness!",
    "Fluffing it up with love!",
    "One moment, making it super kawaii!",
    "Nyah~! Just adding some sparkle!",
    "Oki doki! Extra adorable coming up!",
    "UwU~! Crafting something sweet!",
    "Squee! Almost done with the fluffiness!",
    "Hehe~! Adding a touch of cute!",
    "Giggle~! Wrapping it in sweetness!",
    "Wheee~! Making it extra snuggly!",
    "Pwease wait! Adding a kawaii touch!",
    "Yay! Almost ready, with a sprinkle of magic!",
    "Teehee~! Just a moment, making it extra cute!",
    "Almost there! Adding a dash of whimsy!",
    "Eep! Turning it into a bundle of joy!",
    "Just a sec~! Making it sparkle!",
    "Hooray! Adding some extra charm!",
    "Hang tight! Crafting something delightful!",
    "Aww~! Almost done with the cuteness!",
    "Meow~! Just fluffing it up!",
    "Yippee! Almost ready with a touch of magic!",
    "Choo! Preparing something adorable!",
    "Oh my! Adding extra charm and fluff!",
    "Eee! Almost there, making it super sweet!",
    "Phew! Just adding the final touches of cuteness!"
]

def load_list(file_path):
    if os.path.exists(file_path):
        try:
            with open(file_path, 'r') as file:
                return json.load(file)
        except (json.JSONDecodeError, FileNotFoundError):
            print("Error1.")
            return []  # Return an empty list if there is an error
    else:
        print("Error2.")
        return []

kosmos = load_list("kosmos.json")
#print(kosmos)

async def save(message, list, aimessage):
    list.append({
        "role": "user",
        "content": message.content
    })
    list.append({
        "role": "assistant",
        "content": aimessage
    })

async def handle_message(message):
    #if isinstance(message.channel, (discord.DMChannel, discord.GroupChannel)) and message.author != bot.user:
    if message.author != bot.user:
            print(f"{message.author.name} said: {message.content}")
            dmessage = await message.channel.send(random.choice(responses))
            
            if message.author.id == 456404988290269184:
                aimessage = await LocalUwuifyStream(kosmos, dmessage, message)
                await save(message, kosmos, aimessage)
            #audio = tts.get_audio(aimessage)
            #await message.channel.send(file=discord.File(audio, 'tts.mp3'))

@bot.event
async def on_message(message):
    if message.content[1:].startswith(".") or message.content[1:].startswith("!"):
        await bot.process_commands(message)
        return
    if isinstance(message.channel, (discord.DMChannel, discord.GroupChannel)):
        if len(message.content) >= 3:
            await handle_message(message)
    await bot.process_commands(message)

try:
    print("Running. Press Ctrl+C to save and exit.")
    bot.run("niggathought.g.g.g")
except KeyboardInterrupt:
    print("Interrupted by user.")
finally:
    with open('kosmos.json', 'w') as file:
        json.dump(kosmos, file, indent=4)
    print("Data saved to kosmos.json")
