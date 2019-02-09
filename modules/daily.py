import discord
from discord.ext import commands
import random
import math
from datetime import datetime
from discord.ext.commands.cooldowns import BucketType
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw



class Daily:
	def __init__(self,bot):
		self.bot = bot




	def timeLeft(self,seconds):
		if seconds < 60:
			return "{}s".format(seconds)
		else:
			minutes = int(seconds/60)
			secremain = int(seconds - (minutes * 60))
			if minutes >= 60:
				hours = int(minutes/60)
				minremain = int(minutes - (hours * 60))
				if hours >= 24:
					days = int(hours/24)
					hoursremain = int(hours - (days * 24))
					return "{}D {}H {}M {}S ".format(days,hoursremain,minremain,secremain)
				else:
					return "{}H {}M {}S ".format(hours,minremain,secremain)
			else:
				return "{}M {}S".format(minutes,secremain)


	@commands.command(name="daily")
	@commands.cooldown(rate=1, per=86400, type=commands.BucketType.user)
	async def _daily(self,ctx):
		"""
		Description
		-----------
		Earn 350 credits and 1 key to gain access to ?box

		Usage
		-----
		?daily
		"""
		async with self.bot.db.acquire() as con:
			userD = await con.fetchrow(f"SELECT * FROM user_table WHERE user_id={ctx.author.id}")
			if userD:
				try:
					#update the information for daily; it should really all be moved but cant really do it atm
					await con.execute(f"UPDATE user_eco SET credits=credits + 350 WHERE user_id={ctx.author.id}")
					# await con.execute(f"UPDATE user_table SET crates=crates + 1 WHERE user_id={ctx.author.id}")
					await con.execute(f"UPDATE users_daily SET uses=uses + 1 WHERE user_id={ctx.author.id}")
					boxd = await con.fetchrow(f"SELECT crates FROM user_table WHERE user_id={ctx.author.id}")

					#then we need to create the image with the users id
					image = Image.open("/root/community/images/daily.png")
					draw = ImageDraw.Draw(image)
					fontbig = ImageFont.truetype("/root/community/fonts/trench.otf",45)
					fontsmall = ImageFont.truetype("/root/community/fonts/trench.otf",32)
					draw.text((35,35),str(ctx.author.name),(255,255,255),font=fontbig)
					draw.text((83,83),"Collected 350 Credits!",(255,255,255),font=fontsmall)
					image.save("/root/community/images/daily2.png")#save the image as daily2.png so we can reuse the first one
					await ctx.send(content=None,file=discord.File("/root/community/images/daily2.png"))

					if boxd['crates'] >=8:
						cratesgiven = 0 
						fmt = "`You earned no keys as you have reached the limit of 8 keys.`"
					else:
						cratesgiven = 1
						fmt = f"`You earned 1 key giving you a total of {boxd['crates'] +1} to use with ?box`"
					await con.execute(f"UPDATE user_table SET crates=crates + {cratesgiven} WHERE user_id={ctx.author.id}")
					await ctx.send(fmt)
				except Exception as er:
					await ctx.send(er)
			else:
				await ctx.send("`There was an issue fetching your data please tell twitch.`")
		await self.bot.db.release(con)


	@_daily.error
	async def daily_error(self,ctx,error):
		if isinstance(error,commands.CommandOnCooldown):
			await ctx.send(f"```fix\n You can collect your daily in {self.timeLeft(error.retry_after)}```")
		else:
			await ctx.send(error)



def setup(bot):
	bot.add_cog(Daily(bot))
