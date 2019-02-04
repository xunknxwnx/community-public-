import discord, os, asyncpg, asyncio, logging
from discord.ext import commands
from include import config 
from datetime import datetime
import logging
import aqualink


class Community(commands.Bot):
	def __init__(self):
		super().__init__(command_prefix="?")
		self.config = config
		self.launch_time = datetime.utcnow()
		self.startup_extensions = ['modules.daily','modules.box','modules.Owner','modules.Songs','modules.Events','jishaku','modules.WaveLinkMusic']
		self.path = os.path.dirname(os.path.realpath(__file__))



	async def start_db(self):
		self.db = await asyncpg.create_pool(dsn=self.config.dsn)

	async def on_ready(self):
		await self.start_db()
		print("database started")
		# await self.start_lavalink()
		# print("started lavalink")
		await self.startup_extensions()
		print("aqualink connected")
		print("=========================|")
		print("Community Bot Is Online! |")
		print("-------------------------|")
		print(f"D.py Version {discord.__version__}")
		print("=========================|")
		self.loop.create_task(self.presence())


	async def presence(self):
		"""presence loop"""
		await self.wait_until_ready()
		while not self.is_closed():
			await self.change_presence(
				status= discord.Status.dnd,
				activity= discord.Streaming
					name = random.choice(
						(
						# f"?help |{len(self.users)} Users"
						# f"{len(self.guilds)} guilds",
						# f"{len(self.users)} users",
						# f"MOTD: ?daily is gone still",
                        )
                    ),
                    url="https://twitch.tv/streamer",
                )
			await asyncio.sleep(35)


	def run(self):
		loaded =0
		self.remove_command('help')
		for extension in self.startup_extensions:
			try:
				self.load_extension(extension)
				loaded +=1
			except Exception as er:
				print(er)
		print(f"LOADED {loaded} COGS")

		super().run(self.config.token,reconnect=True)


if __name__ == "__main__":
	Community().run()