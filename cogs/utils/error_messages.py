import discord
from discord.ext import commands
import datetime
import cogs.utils.server_prefix_manager as prefix

async def cooldown_error(ctx: commands.Context, error):
    remaining = round(error.retry_after, 1)
    total = round(error.cooldown.per)

    embed_dict = {
        "color": 16727378,
        "footer": {
            "text": f"Default Cooldown: {total} seconds"
        },
        "fields": [
            {
                "name": "Chill out bro",
                "value": f"That command is on cooldown for **{remaining}** more seconds!"
            }
        ]
    }

    message = discord.Embed.from_dict(embed_dict)
    await ctx.send(embed=message)

async def missingargument_error(ctx: commands.Context, error: commands.MissingRequiredArgument, responseDict, correctFormat):
    commandPrefix = prefix.getGuildPrefixFromID(ctx.guild.id)
    date_string = datetime.datetime.now().strftime("%#I:%M %p")
    embed_dict = {
        "color": 15444010,
        "footer": {
            "text": f"Invoked by {ctx.author.name} • {date_string}"
        },
        "fields": [
            {
                "name": responseDict[str(error.param.name)],
                "value": f"{commandPrefix}{correctFormat}"
            }
        ]
    }
    message = discord.Embed.from_dict(embed_dict)
    await ctx.send(embed=message)

async def missingpermission_error(ctx: commands.Context, error: commands.MissingPermissions):
    commandPrefix = prefix.getGuildPrefixFromID(ctx.guild.id)
    date_string = datetime.datetime.now().strftime("%#I:%M %p")

    missing = [perm.replace('_', ' ').replace('guild', 'server').title() for perm in error.missing_perms]

    if len(missing) > 2:
        missing_permissions = '{}, and {}'.format(", ".join(missing[:-1]), missing[-1])
    else:
        missing_permissions = ' and '.join(missing)

    embed_dict = {
        "color": 16727378,
        "footer": {
            "text": f"Invoked by {ctx.author.name} • {date_string}"
        },
        "fields": [
            {
                "name": "Missing Permissions",
                "value": f"You need **{missing_permissions}** permission(s) to run this command."
            }
        ]
    }

    message = discord.Embed.from_dict(embed_dict)
    await ctx.send(embed=message)