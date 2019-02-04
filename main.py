import discord, os, asyncpg, asyncio, random
from discord.ext import commands
from include import config 
from datetime import datetime
import aqualink


class Community(commands.Bot):
	def __init__(self):
		super().__init__(command_prefix=config.prefix)
		aqualink.Connection(self)
		self.config = config
		self.launch_time = datetime.utcnow()
		self.startup_extensions = ['jishaku',
									'modules.box',
									'modules.daily',
									'modules.events',
									'modules.album',
									'modules.Songs',
									'modules.music',
									'modules.owner',
									'modules.shop',
									'modules.misc'
									# 'modules.another'
									]
		self.path = os.path.dirname(os.path.realpath(__file__))



	async def start_aqua(self):
		"""starts aqua"""
		aqualink.Connection.connect_to(self)
		try:
			await self.aqualink.connect(password="youshallnotpass",
										ws_url="ws://localhost:2333",
										rest_url="http://localhost:2333"
										)
		except Exception as er:
			print(er)


	async def start_db(self):
		self.db = await asyncpg.create_pool(dsn=self.config.dsn)

	async def on_ready(self):
		try:
			await self.start_db()
			DBSTATUS = "DB LOADED"
		except:
			DBSTATUS = "FAILED LOADING DB"
		await self.start_aqua()
		print("+=========================+")
		print("|Community Bot Is Online! |")
		print("|-------------------------|")
		print(f"|D.py Version {discord.__version__}")
		print(f"|{self.loaded}/{len(self.startup_extensions)} Cogs Loaded!")
		print("+=========================+")
		self.loop.create_task(self.presence())
		await self.get_channel(540291689374285825).send(f"`Bot is online with {self.loaded}/{len(self.startup_extensions)} modules loaded`")

	async def presence(self):
		while not self.is_closed():
			await self.change_presence(
				activity=discord.Streaming(
					status=discord.Status.dnd,
					name=random.choice(
						(
						f"?help",
						f"{len(self.guilds)} Servers",
						f"{len(self.users)} users",
						f"MOTD: SAT 2PM EST",
						f"{len(self.commands)} Commands"
                        )

					),
					url="https://www.twitch.tv/streamer",
				),
			)
			await asyncio.sleep(45)


	def run(self):
		loaded =0
		self.remove_command('help')
		for extension in self.startup_extensions:
			try:
				self.load_extension(extension)
				loaded +=1
			except Exception as er:
				print(er)
		self.loaded = loaded
		print(f"Loaded {loaded} Cogs")

		super().run(self.config.token,reconnect=True)


if __name__ == "__main__":
	Community().run()
