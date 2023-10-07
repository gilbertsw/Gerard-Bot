import discord
import src.responses as responses
from discord_client import client
from src.log import logger
from helper import env_helper, file_helper
 
def run_discord_bot():
    # intents = discord.Intents.default()
    # intents.message_content = True
    # client = discord.Client(intents=intents)

    @client.event
    async def on_ready():
        await client.send_main_prompt()
        await client.tree.sync()
        logger.info(f'{client.user} is now running')


    @client.event
    async def on_message(message):
        if message.author == client.user:
            return
        
        username = str(message.author)
        user_message = str(message.content)
        channel = str(message.channel)
        logger.info(f'{username} said: "{user_message}" on {channel}')

        # Get ChatGPT response
        response = responses.get_response(user_message)

        if client.is_private:
            await message.author.send(response)
        elif client.user.mentioned_in(message):
            await message.channel.send(response)
    

    @client.tree.command(name="help", description="Show help for the bot")
    async def help(interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=False)
        await interaction.followup.send(file_helper.get_help)
    

    @client.tree.command(name="private", description="Toggle private access")
    async def private(interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=False)
        if not client.is_private:
            client.is_private = not client.is_private
            logger.warning("\x1b[31mSwitch to private mode\x1b[0m")
            await interaction.followup.send(
                "> **INFO: Next, the response will be sent via private reply. If you want to switch back to public mode, use `/public`**")
        else:
            logger.info("You already on private mode!")
            await interaction.followup.send(
                "> **WARN: You already on private mode. If you want to switch to public mode, use `/public`**")


    @client.tree.command(name="public", description="Toggle public access")
    async def public(interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=False)
        if client.is_private:
            client.is_private = not client.is_private
            await interaction.followup.send(
                "> **INFO: Next, the response will be sent to the channel directly. If you want to switch back to private mode, use `/private`**")
            logger.warning("\x1b[31mSwitch to public mode\x1b[0m")
        else:
            await interaction.followup.send(
                "> **WARN: You already on public mode. If you want to switch to private mode, use `/private`**")
            logger.info("You already on public mode!")
    
    
    # Run Discord Client
    TOKEN = env_helper.get('DISCORD_TOKEN')
    client.run(TOKEN)
