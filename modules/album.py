import discord
from discord.ext import commands



class Albums:
	def __init__(self,bot):
		self.bot = bot
		self.albumids = [534919397240995850,
						536547824909811742,
						536547879205077032,
						536547924751024156,	
						536547970145845253,
						536548002861416449,
						536548056221351938,
						536548092560932866,
						536548142246789123,
						536548207426011136,
						536547824909811742]


	async def process_roles(self,ctx,roleOBJ):
		"""
		The for loop that i need to remove the roles from the user and give them a new one
		but simplified to its easier to finish this code; It's done like this so i can finish
		the code in a smaller amount of time but also simplifies expansion of the list of roles
		well kindda.
		"""
		yes = None
		for i in ctx.author.roles:
			if i.id in self.albumids:#if there is a role inside of the id list it sets a value to true which i then compare to so that the use ends up with a role
				await ctx.author.remove_roles(i)
				await ctx.author.add_roles(roleOBJ)
				await ctx.send(f"`You now have the {roleOBJ.name} Role!`")
				yes = True
			else:
				pass
		if yes !=True:
			await ctx.author.add_roles(roleOBJ)
			await ctx.send(f"`You now have the {roleOBJ.name} Role!`")
		else:
			pass
		return True


	@commands.command(name="album")
	async def _album(self,ctx, *,specific:str=None):
		"""
		Description
		-----------
		Ability to equip a role earned in the shop

		Usage
		-----
		?album [name here]

		Example
		-------
		?album the now now
		"""
		helperRole = discord.utils.get(ctx.guild.roles,id=529049551705735169)
		if ctx.channel.id ==529055788665143343 or helperRole in ctx.author.roles:
			async with self.bot.db.acquire() as con:
				query1 = "SELECT * FROM album_roles WHERE user_id=$1 and role=$2"
				yes = None
				if specific == None:
					query = "SELECT role FROM album_roles WHERE user_id=$1"
					albumD = await con.fetch(query,int(ctx.author.id))
					if albumD:
						for i in ctx.author.roles:
							if i.id in self.albumids:
								await ctx.author.remove_roles(i)
							else:
								pass
						text = ""
						for a in albumD:
							text += f"<@&{str(a['role'])}>\n"

						return await ctx.send(embed=discord.Embed(title="Your roles:",description=text))
					else:
						return await ctx.send("`You own no album roles visit #shop to buy some!`")


				if specific.lower() == "the now now":
					# print("hi")
					userd = await con.fetchrow(query1,int(ctx.author.id),534919397240995850)
					# print("hi2")
					nowRole = discord.utils.get(ctx.guild.roles,id=534919397240995850)
					if userd:
						# print("hi3")
						for i in ctx.author.roles:
							if i.id in self.albumids:
								await ctx.author.remove_roles(i)
								await ctx.author.add_roles(nowRole)
								await ctx.send("`You now have The Now Now role!`")
								yes = True
							else:
								pass
						if yes !=True:
							await ctx.author.add_roles(nowRole)
							await ctx.send("`You now have The Now Now role!`")
						else:
							pass
					else:
						await ctx.send("`You do not own this role!`")

				elif specific.lower() == "glory sound prep":
					userD = await con.fetchrow(query1,int(ctx.author.id),536547824909811742)
					gloryRole = discord.utils.get(ctx.guild.roles,id=536547824909811742)
					if userD:
						await self.process_roles(ctx,gloryRole)
					else:
						await ctx.send("`You do not own this role!`")

				elif specific.lower() == "never nothing":
					userD = await con.fetchrow(query1,int(ctx.author.id),536547879205077032) 
					neverRole = discord.utils.get(ctx.guild.roles,id=536547879205077032)
					if userD:
						await self.process_roles(ctx,neverRole)
					else:
						await ctx.send("`You do not own this role!`")

				elif specific.lower() == "nice colors":
					userD = await con.fetchrow(query1,int(ctx.author.id),536547924751024156) 
					niceRole = discord.utils.get(ctx.guild.roles,id=536547924751024156)
					if userD:
						await self.process_roles(ctx,niceRole)
					else:
						await ctx.send("`You do not own this role!`")

				elif specific.lower() == "ballads 1":
					userD = await con.fetchrow(query1,int(ctx.author.id),536547970145845253) 
					balladsRole = discord.utils.get(ctx.guild.roles,id=536547970145845253)
					if userd:
						await self.process_roles(ctx,balladsRole)
					else:
						await ctx.send("`You do not own this role`")

				elif specific.lower() == "iridescence":	
					userD = await con.fetchrow(query1,int(ctx.author.id),536548002861416449) 
					iriRole = discord.utils.get(ctx.guild.roles,id=536548002861416449)
					if userD:
						await self.process_roles(ctx,iriRole)
					else:
						await ctx.send("`You do not own this role`")

				elif specific.lower() == "1981 extended play":
					userD = await con.fetchrow(query1,int(ctx.author.id),536548056221351938) 
					playRole = discord.utils.get(ctx.guild.roles,id=536548056221351938)
					if userD:
						await self.process_roles(ctx,playRole)
					else:
						await ctx.send("`You do not own this role`")

				elif specific.lower() == "talking is hard":
					userD = await con.fetchrow(query1,int(ctx.author.id),536548092560932866)
					hardRole = discord.utils.get(ctx.guild.roles,id=536548092560932866)
					if userD:
						await self.process_roles(ctx,hardRole)
					else:
						await ctx.send("`You do not own this role`")

				elif specific.lower() == "reborn":
					userD = await con.fetchrow(query1,int(ctx.author.id),536548142246789123)
					rebronRole = discord.utils.get(ctx.guild.roles,id=536548142246789123)
					if userD:
						await self.process_roles(ctx,rebronRole)
					else:
						await ctx.send("`You do not own this role`")

				elif specific.lower() == "double dare":
					userD = await con.fetchrow(query1,int(ctx.author.id),536548207426011136)
					dareRole = discord.utils.get(ctx.guild.roles,id=536548207426011136)
					if userD:
						await self.process_roles(ctx,dareRole)
					else:
						await ctx.send("`You do not own this role`")
				else:
					await ctx.send("`Role not found`")

			await self.bot.db.release(con)
		else:
			try:
				await ctx.message.delete()
			except:
				pass
			finally:
				await ctx.send("Please use this in <#529055788665143343>",delete_after=6)


def setup(bot):
	bot.add_cog(Albums(bot))