import discord
from discord import app_commands

import helper.file_helper as file_helper

class DiscordClient(discord.Client):
    def __init__(self) -> None:
        intents = discord.Intents.default()
        intents.message_content = True
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)
        self.activity = discord.Activity(type=discord.ActivityType.listening, name="/chat | /help")
        self.is_private = False
        self.main_prompt = file_helper.get_main_prompt()

# Expose client object for app to import
client = DiscordClient()