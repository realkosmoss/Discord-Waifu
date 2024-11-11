from discord.ext import commands
import discord
# the ai shit
import aiohttp
import asyncio
from datetime import datetime
#import pytz # because of you kropka.... "WHY THE FUCK YOU USE PYTZ LMAO WHAT IS THAT?" 😭

# Windows only
import ctypes
def swt(title):
    ctypes.windll.kernel32.SetConsoleTitleW(title)

bot = commands.Bot(command_prefix='omg??theComandPrefixBecuaseItNeedsItOmg')
# Why not?
session = None
async def GetSession():
    global session
    session = aiohttp.ClientSession(trust_env=True, timeout=aiohttp.ClientTimeout(total=0))

# fuck that shit lol
OwnerID = 456404988290269184
PrivateMode = True # if other people other than owner id can chat with the ai
OllamaAPI = "" # the fucking shit u get from the colab.google.com ipybnbfi real. Example: https://frozen-retard-on-crack.trycloudflare.com do not include the / at the end
AI_IN_USE = False
AI_TIME = 0

OwnerData = []
tables = {} # for public use.
def create_table(name):
    tables[name] = []
def add_to_table(name, data):
    if name in tables:
        tables[name].append(data)
    else:
        print(f"Table '{name}' Well something fucked up with the table. im not fixing it")
def get_table(name):
    return tables.get(name, None)

@bot.event
async def on_ready():
    custom_status = discord.CustomActivity(name="✧･ﾟ: *♡ Kawaii and Loving *:･ﾟ✧", emoji="sparkling_heart")
    await bot.change_presence(status=discord.Status.online, activity=custom_status)
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')
    print()

async def Niggerify(messages, dmessage, ogmessage): # OP
    global AI_IN_USE, AI_TIME
    AI_IN_USE = True
    swt(f"Discord AI - Last AI Time: {AI_TIME} - Being Used: {AI_IN_USE}")
    url = OllamaAPI + "/create"
    payload = {
        "messages": messages,
        "message": ogmessage.content # the discord message
    }
    
    try:
        ai_info = None
        async with session.post(url, json=payload, headers = {"Content-Type": "application/json"}) as response:
            response.raise_for_status()
            ai_info = await response.json()
            message = ai_info['message']['content']
            AI_TIME = int(ai_info.get("total_duration", 0)) / 1e9 if ai_info.get("total_duration") else 0

        await dmessage.edit(content=f"<@{ogmessage.author.id}>\n{message}")
        AI_IN_USE = False
        swt(f"Discord AI - Last AI Time: {AI_TIME} - Being Used: {AI_IN_USE}")
        return message
    except Exception as e:
        print("Failed in ai procesing: " + str(e))
        await dmessage.delete()

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
    global OwnerData
    if not session:
        await GetSession()
    if message.author != bot.user:
        ct = datetime.now().strftime("%H:%M")
        print(f"{ct} | Interacted With AI: {message.author.name}")
        if PrivateMode == True:
            if message.author.id == OwnerID:
                try:
                    dmessage = await message.reply("stupid baka") # im killing myself tommorow
                    aimessage = await Niggerify(OwnerData, dmessage, message)
                    await save(message, OwnerData, aimessage)
                except Exception as e:print(e)
        else: # idk fuck you lol
            name = message.author.name
            if not get_table(name):
                userdata = create_table(name)
            else:
                userdata = get_table(name)
            dmessage = await message.reply("stupid baka") # im killing myself tommorow
            aimessage = await Niggerify(userdata, dmessage, message)
            save(message.content, userdata, aimessage) # NO WAY! im not adding resets suck my cock (i removed it and its lost)

@bot.event
async def on_message(message):
    #if isinstance(message.channel, (discord.DMChannel, discord.GroupChannel)):
    if len(message.content) >= 3: # fixes some shit bugs
        await handle_message(message)
    await bot.process_commands(message)

try:
    print("Running. Press Ctrl+C to save and exit.")
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    bot.run("hell nah")
except KeyboardInterrupt:
    print("Interrupted by user.")
