from discord.ext import commands
from discord.ext.commands import BucketType
import cogs.utils.server_prefix_manager as pm

class Admin(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    @commands.command(name="prefix")
    @commands.cooldown(rate=1, per=30, type=BucketType.guild)
    async def prefix(self, ctx: commands.Context, prefix: str):
        pm.setPrefixGuild(ctx.guild.id, prefix)
        await ctx.send(f"Changed prefix to: **\"{pm.getGuildPrefixFromID(ctx.guild.id)}\"**")

    @prefix.error
    async def prefix_error(self, ctx: commands.Context, error):
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.send(f"This command is on cooldown for **{round(error.retry_after)}** more seconds.")
        print(error)

def setup(client):
    client.add_cog(Admin(client))