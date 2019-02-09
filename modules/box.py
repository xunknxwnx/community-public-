import discord
from discord.ext import commands
import random
import math
from datetime import datetime
from discord.ext.commands.cooldowns import BucketType




class Box:
	def __init__(self,bot):
		self.bot = bot
		self.difficulty = 600
		self.roleids = [529417807947890709,
						529418405023973376,
						529418405950914580,
						529418406550700032,
						529418413274038303,
						529418412544360467,
						529418406706020363,
						529418407917912074,
						529422267600470037,
						529422269882040331,
						529422270175903764,
						529422270876090370,
						529422269110419456,
						529418405019648001,
						529418404025860096,
						529425959837761537,
						529426123222810626,
						529425959170867220,
						529424985010339840,
						529425961452568616,
						529426756910841857,
						529426755338108938,
						529426755929505794,
						529425961037332492,
						529426757099585546,
						529426758412271626,
						529429942685925387,
						529429940060291079,
						529429940794556426,
						529431798497673236,
						529425960274231296,
						529425957745066044,
						529434186784702496,
						529434187996987412]


	async def chooserole(self,ctx,roleD):
		"""rolls the box with chances of getting a role; its a function so i can reroll."""
		notRole = []#an empty list later to be filled with roles the user cannot be given
		for role in roleD:#iterates through the roles that the user has in the database then appends them to a list
			notRole.append(role['role'])
		randomID= self.roleids[random.randint(0,len(self.roleids)-1)]#randomly picks an id from the list of song roles.

		if randomID not in notRole:#if the role isnt in the list return the id to used later inside of the command.
			return randomID
		else:
			return None


	@commands.command(name="box")
	# @commands.is_owner()
	@commands.cooldown(rate=1, per=3, type=commands.BucketType.user)
	async def _box(self,ctx):
		"""
		Description
		-----------
		you can uh get roles????

		Usage
		----
		?box
		
		Permissions
		-----------
		No permissions reqired
		"""
		async with self.bot.db.acquire() as con:
			# if ctx.author.id !=440113725970710528:
			# 	return await ctx.send(":crab: box is dead :crab:")
			keysD = await con.fetchrow(f"SELECT crates FROM user_table WHERE user_id={ctx.author.id}")
			keys = keysD['crates']
			if keys < 1 :
				return await ctx.send("`You have no more keys!`")
			roleD = await con.fetch(f"SELECT role FROM roles_table WHERE user_id={ctx.author.id}")
			if keys >=1:
				choice = random.randint(0,1000)
				if choice >= 630:
					randomRole = await self.chooserole(ctx,roleD)
					if randomRole == None:
						randomRole = await self.chooserole(ctx,roleD)
					else:
						pass
					role = discord.utils.get(ctx.guild.roles,id=randomRole)
					fmt = f"You won the <@&{role.id}> Role!"
					embed = discord.Embed(title=None,description=fmt,colour=0x5b2076)
					try:
						await con.execute(f"INSERT INTO roles_table (user_id,role) VALUES ({ctx.author.id},{randomRole})")
					except:
						await ctx.send("`There was an error giving you your role please tell twitch`")
					await ctx.send(embed=embed)
				else:
					await ctx.send(embed=discord.Embed(title=None,description="`You won nothing :(`",colour=0x5b2076))

			await con.execute(f"UPDATE user_table SET crates=crates-1 WHERE user_id={ctx.author.id}")
		if keys - 1 == 0:
			fmt = "`You have no more keys`"
		elif keys -1 == 1:
			fmt = "You have 1 more key"
		else:
			fmt = f"You have {keys - 1} more keys"
		await ctx.send(fmt)

		await self.bot.db.release(con)


	@_box.error
	async def box_error(self,ctx,error):
		await ctx.send(f"```fix\n{error}```")


		












def setup(bot):
	bot.add_cog(Box(bot))