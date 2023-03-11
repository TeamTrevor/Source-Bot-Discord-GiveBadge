import requests
import json
import inspect
import sys
import os

from colorama import Fore, Style

import discord
from discord.ext.commands import Bot
from discord.ext import commands
import asyncio

if sys.version_info < (3, 8):
    exit("Python 3.8 or higher is required to run this bot!")

try:
    from discord import app_commands, Intents, Client, Interaction
except ImportError:
    exit(
        "Either discord.py is not installed or you are running an older and unsupported version of it."
        "Please make sure to check that you have the latest version of discord.py! (try reinstalling the requirements?)"
    )

try:
    with open("config.json") as f:
        config = json.load(f)
except (FileNotFoundError, json.JSONDecodeError):
    config = {}


while True:
    token = config.get("token", None)
    if token:
        print(f"\n--- Detected token in {Fore.GREEN}./config.json{Fore.RESET} (saved from a previous run). Using stored token. ---\n")
    else:
        token = input("> ")

    try:
        data = requests.get("https://discord.com/api/v10/users/@me", headers={
            "Authorization": f"Bot {token}"
        }).json()
    except requests.exceptions.RequestException as e:
        if e.__class__ == requests.exceptions.ConnectionError:
            exit(f"{Fore.RED}ConnectionError{Fore.RESET}: Discord is commonly blocked on public networks, please make sure discord.com is reachable!")

        elif e.__class__ == requests.exceptions.Timeout:
            exit(f"{Fore.RED}Timeout{Fore.RESET}: Connection to Discord's API has timed out (possibly being rate limited?)")

        exit(f"Unknown error has occurred! Additional info:\n{e}")

    if data.get("id", None):
        break

    print(f"\nSeems like you entered an {Fore.RED}invalid token{Fore.RESET}. Please enter a valid token (see Github repo for help).")

    config.clear()

with open("config.json", "w") as f:
    config["token"] = token

    json.dump(config, f, indent=2)


class FunnyBadge(Client):
    def __init__(self, *, intents: Intents):
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self) -> None:
        await self.tree.sync()

client = FunnyBadge(intents=Intents.none())

@client.event
async def on_ready():
    print(inspect.cleandoc(f"""

        [ ONLINE ] LOGIN {client.user} [ ID: {client.user.id} ]
        [ SYSTEM ] INVITE ME {client.user} TO YOUR SERVER:
        https://discord.com/api/oauth2/authorize?client_id={client.user.id}&scope=applications.commands%20bot
    """), end="\n\n")

    activity = discord.Game(name="/help | ZERO", type=3)
    await client.change_presence(status=discord.Status.idle, activity=activity)

# Commands --------------------------------------------------------------------

@client.tree.command(description="Sends the bot's latency.")
async def help(interaction: Interaction):
    print(f"> {Style.BRIGHT}{interaction.user}{Style.RESET_ALL} used the command.")

    embed = discord.Embed(title="สวัสดีครับ / ค่ะ", url="", description=f"<@{interaction.user.id}>\nหากต้องการดูคำสั่ง ดูข้างล่างเลย!!", color=discord.Color.green())
    embed.add_field(name=f"COMMAND | {interaction.user}", value="/help | /hello", inline=False)
    await interaction.response.send_message(embed = embed)

@client.tree.command()
async def hello(interaction: Interaction):
    print(f"> {Style.BRIGHT}{interaction.user}{Style.RESET_ALL} used the command.")

    embed = discord.Embed(title="สวัสดีครับ / ค่ะ", url="", description=f"<@{interaction.user.id}>\nหากต้องการดูรายชื่อพัฒนา ดูข้างล่างเลย!!", color=discord.Color.blue())
    embed.add_field(name="DEVELOPER", value="! ZERO </> #1937", inline=True)
    embed.add_field(name="DEVELOPER", value="wait#3561", inline=True)
    await interaction.response.send_message(embed = embed)

client.run(token)