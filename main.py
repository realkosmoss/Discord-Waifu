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
    "Let me sprinkle some magic on that!",
    "Just a moment, making it extra adorable for you!",
    "Puffing up a sweet reply!",
    "Hold on! Crafting a cuteness overload just for you!",
    "Adding a touch of kawaii to your request!",
    "Nyah~! Turning it into pure adorableness!",
    "Oki doki! Making it super duper cute, just for you!",
    "UwU~! Let me fluff it up with some love!",
    "Squee! Just a sec, filling it with extra sparkles!",
    "Hehe~! Making it as cuddly as a plushie!",
    "Giggle~! Adding all the sweetness just for you!",
    "Wheee~! Making it so cute you’ll wanna hug it!",
    "Pwease wait! Wrapping it in a bow of cuteness!",
    "Yay! Sprinkle, sprinkle! Almost done with the cuteness!",
    "Teehee~! Just a mo, preparing something super kawaii!",
    "Almost there! Adding some extra sugar and spice!",
    "Eep! Busy turning it into a bundle of joy!",
    "Just a sec~! Making it sparkle with cuteness!",
    "Hooray! Creating something sweet and snuggly!",
    "Hang tight! Filling it with a dash of whimsy!",
    "Aww, wait a moment! Crafting something delightfully sweet!",
    "Meow~! I’m adding extra fluffiness just for you!",
    "Yippee! Almost ready with a sprinkle of magic!",
    "Choo! Preparing a dose of adorable just for you!",
    "Oh my! Just fluffing it up with cuteness overload!",
    "Eee! Almost done, making it so charming and sweet!",
    "Phew! Almost there, adding all the cozy feels!"
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

smolmonke = load_list("smolmonke.json")
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
            
            if message.author.id == 1235290447640006699:
                aimessage = await LocalUwuifyStream(smolmonke, dmessage, message)
                await save(message, smolmonke, aimessage)
            elif message.author.id == 456404988290269184:
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
    with open('smolmonke.json', 'w') as file:
        json.dump(smolmonke, file, indent=4)
    print("Data saved to kosmos.json and smolmonke.json")
