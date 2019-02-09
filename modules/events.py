import discord
from discord.ext import commands
import random
import math
from datetime import datetime



class Events:
	def __init__(self,bot):
		self.bot = bot
		self.reactions =['👍','👎']



	async def on_member_join(self,member):
		"""add the user to a database with their original username and time of joining"""
		async with self.bot.db.acquire() as con:
			#first i need to get a few things
			query = "SELECT * FROM user_table WHERE user_id=$1"
			userd = await con.fetchrow(query,int(member.id))
			if userd:
				return await self.bot.db.release(con)
			if not userd:
				username = str(member.name + "#" + str(member.discriminator))
				userid = int(member.id)
				joinNONFMT = member.joined_at
				jointimeFMT = joinNONFMT.strftime("%b At %H:%M")
				crateamount = 0
				insert = "INSERT INTO user_table (user_id,username,crates,joindate) VALUES ($1,$2,$3,$4)"
				insert2 = "INSERT INTO users_daily (user_id,uses) VALUES ($1,$2)"
				try:
					await con.execute(insert,userid,username,crateamount,jointimeFMT)
					await con.execute(insert2,userid,0)
				except Exception as er:
					print(er)
					print("error inserting to table")

		await self.bot.db.release(con)
		communityGuild = self.bot.get_guild(529042068891238431)
		chan1 = self.bot.get_channel(529081859771203585)
		chan2 = self.bot.get_channel(529081861117575188)
		await chan2.edit(name=f"User Count: {communityGuild.member_count - 2}")
		await chan1.edit(name=f"Member Count: {communityGuild.member_count}")


	async def on_message_delete(self,message):
		if message.author.bot:
			return
		else:
			logChan  = self.bot.get_channel(540606131781763082)
			logchan2 = self.bot.get_channel(541039176796078090)
			if message.content.startswith("?av"):
				return
			try:	
#				url = message.attachments[0].url
#				await logChan.send(url)
				fmt = ("```Json\n"
					f"Channel - {message.channel.name}\n"
					f"Author - {message.author}\n"
					f"Content - {message.content}\n```")
				await logChan.send(fmt)
				await logchan2.send(fmt)
			except Exception as er:
				await logChan.send(er)


def setup(bot):
	bot.add_cog(Events(bot))
