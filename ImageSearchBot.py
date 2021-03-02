import discord
import os
from dotenv import load_dotenv
from io import BytesIO
import sys

from ImageSearch import *

class ImageSearchBot(discord.Client):
	async def upload_query(self, channel, query):
		arr = BytesIO()

		while i := 1 < 4:
			try:
				extension, data = get_first_image(await get_page(get_query_link(query)))
				
				arr.write(data)
				arr.seek(0)

				await channel.send(file = discord.File(arr, filename=f"requested_image.{extension}"))
				break
			
			except Exception as e:
				print(f'Exception in upload query "{query}":', e)
				await channel.send(f"Failed. Trying again ({i})")

		arr.close()
		
	async def on_ready(self):
		await self.change_presence(activity = discord.Activity(type = discord.ActivityType.custom, name = "Mention me with a query"))

		print("I am ready to serve")

	async def on_guild_join(self, guild):
		for channel in guild.text_channels:
			await channel.send(f'Hey! You can search for an image by mentioning me first\nSample usage: "@{self.user.name} <your_query>"')
			await self.upload_query(channel, "heart emoji")

	async def on_message(self, message):
		if message.author == self.user:
			return

		mention_string = f"<@!{self.user.id}>"
		mention_count = message.content.count(mention_string)

		query = None

		if isinstance(message.channel, discord.channel.DMChannel):
			if mention_count > 0:
				await message.channel.send("To search an image via dm, do not use any mentions")
				return
			
			query = message.content
		
		else:
			if mention_count == 0:
				return

			if mention_count > 1 or message.content.find(mention_string) != 0 or len(message.mentions) != 1:
				if self.user.id in [mention.id for mention in message.mentions]:
					await message.channel.send(f'If you want to search for an image, mention me first, then type your query\n"@{self.user.name} <your_query>"')
				return

			query = message.content[len(self.user.name) + 5 : ] # len + 5 for <, >, @, ! and space chars

		await self.upload_query(message.channel, query)

if __name__ == "__main__":
	load_dotenv()
	TOKEN = os.getenv("DISCORD_TOKEN")

	client = ImageSearchBot()

	client.run(TOKEN)
