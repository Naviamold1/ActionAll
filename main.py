from dotenv import load_dotenv
import os
from discord.ext.commands import *
import discord
from discord.ext import commands
from discord.ext.commands import MissingPermissions


load_dotenv()

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix='r!', description='hi', intents=intents)

@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Activity(name='Naviamold!', type=discord.ActivityType.watching))
    print(f'We have logged in as {bot.user}')

@bot.command(name='ping', description='Pong!', force_global=True)
async def pingtest(ctx):
    await ctx.send(f'Pong: {round (bot.latency * 1000)} ms')

@bot.command()
async def kickall(ctx, *, reason=None):
    if ctx.message.author.top_role.permissions.administrator:
        for member in ctx.guild.members:
                try:
                    await member.kick(reason=reason)
                    print(f"✔️ Kicked {member.name}")
                    await ctx.send(f"✔️ Kicked {member.name}")
                except:
                    print(f"❌ Could not kick {member}")
                    await ctx.send(f'❌ Could not kick {member}')
    else:
        await ctx.send("Missing permissions.")

@bot.command()
async def msgall(ctx, *, args=None):
    if args != None:
        members = ctx.guild.members
        for member in members:
            try:
                await member.send(args)
                print(f'✔️ Successfully sent dm to {member}')
                await ctx.send(f'✔️ Successfully sent dm to {member}')
            except:
                await ctx.send(f'❌ Could Sent DM to {member}')
                print(f'❌ Could Sent DM to {member}')


bot.run(os.getenv('BOT_TOKEN'))