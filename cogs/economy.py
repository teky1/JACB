from discord.ext import commands
from discord.ext.commands import BucketType
import cogs.utils.balance_manager as bal
import cogs.utils.error_messages as error_msg
import discord
import typing
import random

class Economy(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    @commands.command(name="balance", aliases=["bal"])
    @commands.cooldown(rate=1, per=2, type=BucketType.user)
    async def balance(self, ctx: commands.Context, who: typing.Optional[discord.Member]):
        who = ctx.author if who is None else who
        balance = bal.getBalance(who.id)
        await ctx.send(f"{who.display_name}'s balance is **{balance}**")

    @balance.error
    async def balance_error(self, ctx: commands.Context, error):
        if isinstance(error, commands.CommandOnCooldown):
            await error_msg.cooldown_error(ctx, error)
        else:
            raise error

    @commands.command(name="beg")
    @commands.cooldown(rate=1, per=30, type=BucketType.user)
    async def beg(self, ctx: commands.Context):
        # 50% chance to give nothing and 50% chance to get between 0-200
        payment = 0 if random.randrange(4) == 1 else random.randrange(50)
        bal.setBalance(ctx.author.id, bal.getBalance(ctx.author.id)+payment)
        if payment == 0:
            await ctx.send(f"{ctx.author.mention} Nobody cared, you got nothing.")
        else:
            await ctx.send(f"{ctx.author.mention}, A kind stranger donated **{payment}**")

    @beg.error
    async def beg_error(self, ctx: commands.Context, error):
        if isinstance(error, commands.CommandOnCooldown):
            await error_msg.cooldown_error(ctx, error)
        else:
            raise error

    @commands.command(name="give", aliases=["donate", "share"])
    @commands.cooldown(rate=1, per=5, type=BucketType.user)
    async def give(self, ctx: commands.Context, target: discord.Member, amount: int):
        if target == ctx.author:
            await ctx.send("You cant give yourself money tf???")
            return
        giver_bal = bal.getBalance(ctx.author.id)
        if giver_bal < amount:
            await ctx.send("You're too broke to give away that much!")
            return
        elif amount <= 0:
            await ctx.send("Why would you wanna give away that little???")
            return

        target_bal = bal.getBalance(target.id)

        bal.setBalance(ctx.author.id, giver_bal-amount)
        bal.setBalance(target.id, target_bal+amount)
        await ctx.send(f"{target.mention}, you have received **{amount}** from {ctx.author.mention}!!!")

    @give.error
    async def give_error(self, ctx: commands.Context, error):
        response_dict = {
            "target": "Who do you want to give money to?",
            "amount": "How much do you want to give?"
        }
        correct_format = "give <@!258048636653535234> <amount>"

        if isinstance(error, commands.CommandOnCooldown):
            await error_msg.cooldown_error(ctx, error)
        elif isinstance(error, commands.MissingRequiredArgument):
            await error_msg.missingargument_error(ctx, error, response_dict, correct_format)
        else:
            raise error

    @commands.command(name="coinflip")
    @commands.cooldown(rate=1, per=3, type=BucketType.user)
    async def coinflip(self, ctx: commands.Context, amount: int):
        didWin = random.random() <= 0.45
        curr_bal = bal.getBalance(ctx.author.id)
        if curr_bal < amount:
            await ctx.send("You're too broke to bet this much!!!")
            return
        elif amount <= 0:
            await ctx.send("Why you tryna bet that little? broke boi")
            return

        if didWin:
            bal.setBalance(ctx.author.id, curr_bal+amount)
            await ctx.send(f"You won the coin toss! You gained **{amount}**! pogchamp")
        else:
            bal.setBalance(ctx.author.id, curr_bal - amount)
            await ctx.send(f"You lost the coin toss! You lost **{amount}**! LLLL")

    @coinflip.error
    async def coinflip_error(self, ctx: commands.Context, error):
        response_dict = {
            "amount": "How much do you want to bet?"
        }
        correct_format = "coinflip <amount>"
        if isinstance(error, commands.CommandOnCooldown):
            await error_msg.cooldown_error(ctx, error)
        elif isinstance(error, commands.MissingRequiredArgument):
            await error_msg.missingargument_error(ctx, error, response_dict, correct_format)
        else:
            raise error


def setup(client):
    client.add_cog(Economy(client))