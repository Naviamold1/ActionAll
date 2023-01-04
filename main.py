import os
import time

import discord
from discord import Interaction, app_commands
from discord.app_commands import AppCommandError
from discord.ext import commands
from discord.ext.commands import *
from dotenv import load_dotenv
from pretty_help import AppMenu, PrettyHelp

load_dotenv()

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

menu = AppMenu(ephemeral=True)

bot = commands.Bot(command_prefix='r!', description='Custom Bot Made By Naviamold',
                   intents=intents, help_command=PrettyHelp(menu=menu))


@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Activity(name='Naviamold!', type=discord.ActivityType.watching))
    print(f'We have logged in as {bot.user}')
    sync = await bot.tree.sync()
    print(f"Synced {len(sync)} commands(s):")
    for item in sync:
        print(item.name)


@bot.tree.command(name="ping", description="Pong")
@app_commands.default_permissions(administrator=True)
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message(f'Pong: {round (bot.latency * 1000)} ms', ephemeral=True)


@bot.tree.command(name="kick_all", description="Kicks Every Member")
@app_commands.default_permissions(administrator=True)
async def kickall(ctx, *, reason: str = None):
    if ctx.message.author.top_role.permissions.administrator:
        for member in ctx.guild.members:
            try:
                await member.kick(reason=reason)
                print(f"✔️ Kicked {member.name}")
                await ctx.send(f"✔️ Kicked {member.name}")
            except:
                print(f"❌ Could not kick {member}")
                await ctx.send(f'❌ Could not Kick {member}')
    else:
        await ctx.send("Missing Permissions.")


@bot.tree.command(name="ban_all", description="Bans Every Member")
@app_commands.default_permissions(administrator=True)
async def banall(ctx, *, reason: str = None):
    if ctx.message.author.top_role.permissions.administrator:
        for member in ctx.guild.members:
            try:
                await member.ban(reason=reason, delete_message_days=7)
                await ctx.send(f'✔️ Banned {member.name}')
            except:
                await ctx.send(f'❌ Could not Ban {member.name}')
    else:
        await ctx.send("Missing Permissions.")


@bot.tree.command(name="msg_all", description="Messages Every Member")
@app_commands.default_permissions(administrator=True)
async def msgall(ctx, *, message: str = None):
    if ctx.message.author.top_role.permissions.administrator:
        if message != None:
            num = 0
            members = ctx.guild.members
            for member in members:
                num += 1
                try:
                    if num > 45:
                        await ctx.send(f'Looks like your server has more than 45 members sorry I have to slow down to not hit the rate limit')
                        time.sleep(30)
                        await member.send(message)
                        await ctx.send(f'✔️ Successfully sent dm to {member} with 30 second delay')
                    elif num < 45:
                        await member.send(message)
                        print(f'✔️ Successfully sent dm to {member}')
                        await ctx.send(f'✔️ Successfully sent dm to {member}')
                except:
                    await ctx.send(f'❌ Could Sent DM to {member}')
                    print(f'❌ Could Sent DM to {member}')
    else:
        await ctx.send("Missing Permissions")


@bot.tree.command(name="reset_nicknames", description="Removes Every Members Nickname")
@app_commands.default_permissions(administrator=True)
async def reset_nicknames(ctx):
    for member in ctx.guild.members:
        try:
            nick = member.nick
            await member.edit(nick=None)
            if nick != None:
                await ctx.send(f" ✔ Reset nickname of {member.name} from {nick} to {member.name}")
        except discord.Forbidden:
            # The bot doesn't have permission to change the nickname of this user
            await ctx.send(f" ❌ Dont have permission to reset nickname of {member.name} from {nick} to {member.name}")
            pass
        finally:
            await ctx.send('Finished')


@bot.tree.error
async def error(interaction: Interaction,
                error: AppCommandError):
    await interaction.response.send_message(error, ephemeral=True)


bot.run(os.getenv('BOT_TOKEN'))
