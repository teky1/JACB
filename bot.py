import discord
import discord_components
from discord.ext import commands
import cogs.utils.server_prefix_manager as prefix

with open("bot_token.txt") as tokenfile:
    token = tokenfile.read()

client = commands.Bot(command_prefix=prefix.get_prefix)


client.load_extension("cogs.admin")
client.load_extension("cogs.economy")
client.run(token)
