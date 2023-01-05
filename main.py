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
    for command in sync:
        print(command.name)
    print(f'\nBot is in {len(bot.guilds)} server(s):')
    for server in bot.guilds:
        print(server.name)


@bot.tree.command(name="ping", description="Pong")
@app_commands.default_permissions(administrator=True)
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message(f'Pong: {round (bot.latency * 1000)} ms', ephemeral=True)


@bot.tree.command(name="kick_all", description="Kicks Every Member")
@app_commands.default_permissions(administrator=True)
@app_commands.describe(bots='If True Bots will also be Kicked', reason="Kick Reason")
async def kickall(interaction: discord.Interaction, reason: str = None, bots: bool = False):
    await interaction.response.defer()
    for member in interaction.guild.members:
        if bots is False:
            if member.bot:
                continue
        try:
            await member.kick(reason=reason)
            print(f"✔️ Kicked {member.name}")
            await interaction.followup.send(f"✔️ Kicked {member.name}")
        except:
            print(f"❌ Could not kick {member}")
            await interaction.followup.send(f'❌ Could not Kick {member}')


@bot.tree.command(name="ban_all", description="Bans Every Member")
@app_commands.describe(bots='If True Bots will also be Banned', reason="Ban Reason", delete_message_days="The number of Days worth of Messages to Delete from the user in the Server.")
@app_commands.default_permissions(administrator=True)
async def banall(interaction: discord.Interaction, reason: str = None, delete_message_days: int = 0, bots: bool = False):
    await interaction.response.defer()
    for member in interaction.guild.members:
        if bots is False:
            if member.bot:
                continue
        try:
            await member.ban(reason=reason, delete_message_days=delete_message_days)
            await interaction.followup.send(f'✔️ Banned {member.name}')
        except:
            await interaction.followup.send(f'❌ Could not Ban {member.name}')


@bot.tree.command(name="msg_all", description="Messages Every Member")
@app_commands.default_permissions(administrator=True)
@app_commands.describe(message="Message you want to Send")
async def msgall(interaction: discord.Interaction, message: str):
    await interaction.response.defer()
    if message != None:
        num = 0
        members = interaction.guild.members
        for member in members:
            if member.bot:
                continue
            num += 1
            try:
                if num > 45:
                    await interaction.followup.send(f'Looks like your server has more than 45 members sorry I have to slow down to not hit the rate limit')
                    time.sleep(30)
                    await member.send(message)
                    await interaction.followup.send(f'✔️ Successfully sent dm to {member} with 30 second delay')
                elif num < 45:
                    await member.send(message)
                    print(f'✔️ Successfully sent dm to {member}')
                    await interaction.followup.send(f'✔️ Successfully sent dm to {member}')
            except:
                await interaction.followup.send(f'❌ Could Sent DM to {member}')
                print(f'❌ Could Sent DM to {member}')


@bot.tree.command(name="reset_nicknames", description="Removes Every Members Nickname")
@app_commands.default_permissions(administrator=True)
@app_commands.describe(bots='If True Bots nicknames will also be Reseted')
async def reset_nicknames(interaction: discord.Interaction, bots: bool = False):
    await interaction.response.defer()
    for member in interaction.guild.members:
        if bots is False:
            if member.bot:
                continue
        try:
            nick = member.nick
            await member.edit(nick=None)
            if nick != None:
                await interaction.followup.send(f" ✔ Reset nickname of {member.name} from {nick} to {member.name}")
        except discord.Forbidden:
            # The bot doesn't have permission to change the nickname of this user
            await interaction.followup.send(f" ❌ Dont have permission to reset nickname of {member.name} from {nick} to {member.name}")
            pass


@bot.tree.error
async def error(interaction: Interaction, error: AppCommandError):
    try:
        await interaction.response.send_message(error, ephemeral=True)
    except discord.errors.InteractionResponded:
        await interaction.followup.send(error, ephemeral=True)


bot.run(os.getenv('BOT_TOKEN'))
