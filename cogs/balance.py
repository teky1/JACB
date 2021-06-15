from discord.ext import commands

class Balance(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

def setup(client):
    client.add_cog(Balance(client))