import discord
from discord.ext import commands
import random
import math
from datetime import datetime
from discord.ext.commands.cooldowns import BucketType
from PIL import Image, ImageSequence, ImageFont, ImageDraw, ImageColor
from io import BytesIO

class Daily(commands.Cog):
	def __init__(self,bot):
		self.bot = bot
		self.allowed = [440113725970710528,270017125815418901,406643416789942298]

	async def execute_daily(self,ctx,credits,crates):
		await self.bot.db.execute(f"UPDATE users_daily set uses = uses + 1 WHERE user_id = {ctx.author.id}")
		await self.bot.db.execute(f"UPDATE user_eco SET credits = credits + {credits} WHERE user_id = {ctx.author.id}")
		await self.bot.db.execute(f"UPDATE user_table SET crates = crates + {1 if not crates else crates} WHERE user_id = {ctx.author.id}")


	async def get_boosters(self,ctx):
		crates = await self.bot.db.fetchrow(f"SELECT cratesboost from users_daily WHERE user_id = {ctx.author.id}")
		# await ctx.send(crates)
		if crates['cratesboost'] == False or crates['cratesboost'] == None:
			crates = 1
		elif crates['cratesboost'] != None:
			crates = 2

		credits = await self.bot.db.fetchrow(f"SELECT creditboost from users_daily WHERE user_id = {ctx.author.id}")
		if credits['creditboost'] == False or credits['creditboost'] == None:
			credits = 250

		elif credits['creditboost'] != None:
			credits = 500
		return credits, crates



	def paste_pfp(self,background,pfp):
		bigsize = (pfp.size[0] * 3, pfp.size[1] * 3)
		pfp.thumbnail((96,96),Image.ANTIALIAS)
		mask = Image.new('L', bigsize, 0)
		draw = ImageDraw.Draw(mask) 
		draw.ellipse((0, 0) + bigsize, fill=255)
		mask = mask.resize(pfp.size, Image.ANTIALIAS)
		pfp.putalpha(mask)
		background.paste(pfp,(11,23), pfp)


	def make_image(self,author,avy,crates,credits):
		with Image.open("/root/community/images/daily_new.png") as background:

			font = ImageFont.truetype("fonts/futura.ttf", 50)
			font2 = ImageFont.truetype('fonts/futura.ttf', 22)

			bgdraw = ImageDraw.Draw(background)

			self.paste_pfp(background,avy)#its a function because i can OKAY!

			boosts = []

			if credits == 500:
				boosts.append("cred_boost.png")
			else:
				pass
			if crates == 2:
				boosts.append("box_boost.png")
			else:
				pass

			for index, boost in enumerate(boosts):
				if index == 0:
					background.paste(Image.open(f'images/{boost}','r'),(9,144))
				if index == 1:
					background.paste(Image.open(f'images/{boost}','r'),(9,167))

			bgdraw.text((126, 51),author.name,(255,255,255),font=font)
			bgdraw.text((129, 151),f"You have collected {credits} credits!",(255,255,255),font=font2)

			"""
			Its returning with bytesio because i am using this whole function in an execitor to not block the bot
			especially with all other timed events that need to not be blocked
			"""


			output = BytesIO()
			background.save(output, "png")
			output.seek(0)
			return output





	@commands.command()
	@commands.cooldown(1,86400,BucketType.user) 
	async def daily(self,ctx):
		await ctx.trigger_typing()

		credits, crates = await self.get_boosters(ctx)
		await self.execute_daily(ctx,credits,crates)
		crateamount = await self.bot.db.fetchrow("SELECT crates FROM user_table WHERE user_id=$1",ctx.author.id)


		async with self.bot.session.get(ctx.author.avatar_url_as(format="png"), raise_for_status=True) as avy:#aiohttp cause we do not stan blocking in this household
			author_avy = Image.open(BytesIO(await avy.read()))

		await ctx.send(file=discord.File(await self.bot.loop.run_in_executor(None, self.make_image, ctx.author, author_avy,crates,credits),filename=f"{ctx.author.id}_daily.png",))#here im running in executor to prevent blocking because we really dont want that.

		await ctx.send(f"`You earned {crates} key giving you a total of {crateamount['crates']} to use with !box`")




def setup(bot):
	bot.add_cog(Daily(bot))
	bot.log.info("[MODULES] Loading daily module")