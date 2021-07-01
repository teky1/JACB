from discord.ext import commands
from discord.ext.commands import BucketType
import cogs.utils.server_prefix_manager as pm
import cogs.utils.error_messages as error_msg

class Admin(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    @commands.command(name="prefix")
    @commands.cooldown(rate=1, per=30, type=BucketType.guild)
    @commands.has_guild_permissions(manage_guild=True)
    async def prefix(self, ctx: commands.Context, prefix: str):
        pm.setPrefixGuild(ctx.guild.id, prefix)
        await ctx.send(f"Changed prefix to: **\"{pm.getGuildPrefixFromID(ctx.guild.id)}\"**")

    @prefix.error
    async def prefix_error(self, ctx: commands.Context, error):
        response_dict = {
            "prefix": "Specify new command prefix"
        }
        correct_format = "prefix <new_prefix>"

        if isinstance(error, commands.CommandOnCooldown):
            await error_msg.cooldown_error(ctx, error)
        elif isinstance(error, commands.MissingRequiredArgument):
            await error_msg.missingargument_error(ctx, error, response_dict, correct_format)
        elif isinstance(error, commands.MissingPermissions):
            await error_msg.missingpermission_error(ctx, error)
        else:
            raise error

def setup(client):
    client.add_cog(Admin(client))