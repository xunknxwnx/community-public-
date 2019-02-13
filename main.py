import discord, os, asyncpg, asyncio, random,logging
from discord.ext import commands
from include import config 
from datetime import datetime
import aqualink


logging.basicConfig(
	level = logging.DEBUG,
	format="[%(asctime)s %(name)s/%(levelname)s]: %(message)s",
	datefmt="%H:%M:%S",
	handlers=[
		logging.FileHandler("logs/main.log","w",encoding='UTF-8'),
		logging.StreamHandler()
		]
)
try:
	logging.getLogger("discord.client").disabled = True
	logging.getLogger("discord.http").disabled = True
	logging.getLogger("discord.gateway").disabled = True
	logging.getLogger("discord.state").disabled = True
	logging.getLogger("asyncio").disabled = True
	logging.getLogger("websockets.protocol").disabled = True
	logging.getLogger("aioredis").disabled = True
finally:
	pass
log = logging.getLogger("Community1.main")
log.info("booted")


class Community(commands.Bot):
	def __init__(self):
		super().__init__(command_prefix=config.prefix)
		aqualink.Connection(self)
		self.log = log
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
			self.log.info("AQUALINK LOADED!")
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
		self.log.info("+=========================+")
		self.log.info("|Community Bot Is Online! |")
		self.log.info("|-------------------------|")
		self.log.info(f"|D.py Version {discord.__version__}")
		self.log.info(f"|{self.loaded}/{len(self.startup_extensions)} Cogs Loaded!")
		self.log.info("+=========================+")
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
						# f"CAH 8TH FEB",
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
