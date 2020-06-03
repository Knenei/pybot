import discord
import os
from discord.ext import commands, tasks
from itertools import cycle
client = commands.Bot(command_prefix=['C.', 'c.'])
client.remove_command('help')
status = cycle(['Watching for commands...',
                'Server IP: ',
                'Probably being coded',
                'Updates soon...'])


@client.event
async def on_ready():
    await client.change_presence(status=discord.Status.online, activity=discord.Game("Starting Up"))
    change_status.start()
    print('System is up and running.')


@tasks.loop(seconds=10)
async def change_status():
   await client.change_presence(activity=discord.Game(next(status)))


@client.event
async def on_member_join(ctx, user):
    print(f'{user.name}#{user.discriminator} joined the server')
    role = discord.utils.get(user.server.roles, name='Guest')
    embed = discord.Embed(
        title='Welcome to TheCatKingdom!',
        description=f'Hello {user}! Welcome to the Discord Server!',
        colour=discord.Colour.green()
    )
    embed.set_author(name=f'{user.name}#{user.discriminator}', icon_url=user.avatar_url)
    channel = client.get_channel(709523289109823570)
    await channel.send(embed=embed)
    await ctx.add_roles(role)


@client.event
async def on_member_remove(user):
    embed = discord.Embed(
        title="Its sad to see you go:'(",
        description=f'Goodbye {user.name}#{user.discriminator}, we hope to see you again!',
        colour=discord.Colour.red()
    )
    embed.set_author(name=f'{user.name}#{user.discriminator}', icon_url=user.avatar_url)
    channel = client.get_channel(716124863839993886)
    await channel.send(embed=embed)


@client.command()
async def ping(ctx):
    await ctx.send(f'Pong!\n**Latency**: {round(client.latency*1000)}ms')


@client.command()
@commands.has_permissions(manage_messages=True)
async def clear(ctx, a: int, b=1000):
   if a > b:
       await ctx.send('Value Has To Be Less Than or Equal To 1000')
       return
   else:
       await ctx.channel.purge(limit=a+1)


@clear.error
async def clear_error(ctx, error):
   if isinstance(error, commands.MissingPermissions):
       await ctx.send('**Command**:\nMissing Manage Messages permission')
   elif isinstance(error, commands.MissingRequiredArgument):
       await ctx.send('**Command**:\n`b.clear #`\n                  ^\n**Missing Value**')


@client.command()
@commands.has_permissions(manage_messages=True)
async def purge(ctx, a: int, b=1000):
   if a > b:
       await ctx.send('Value Has To Be Less Than or Equal To 1000')
       return
   else:
       await ctx.channel.purge(limit=a+1)


@purge.error
async def purge_error(ctx, error):
   if isinstance(error, commands.MissingPermissions):
       await ctx.send('**Command**:\nMissing manage messages permission')
   elif isinstance(error, commands.MissingRequiredArgument):
       await ctx.send('**Command**:\n`b.purge #`\n                  ^\n**Missing Value**')


@client.command(aliases=['Kick', 'KICK', 'KIck', 'KICk'])
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, *, reason=None):
    await member.kick(reason=reason)
    await ctx.channel.purge(limit=1)
    channel = client.get_channel(716124863839993886)
    await channel.purge(limit=1)
    await ctx.send(f'Kicked {member} for {reason}\n{member.mention}')
    embed = discord.Embed(
        title="Its sad to see you go:'(",
        description=f'But goodbye {member.name}#{member.discriminator}, next time you come please follow the rules!',
        colour=discord.Colour.red()
    )
    embed.set_author(name=f'{member.name}#{member.discriminator}', icon_url=member.avatar_url)
    await channel.send(embed=embed)


@kick.error
async def kick_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send('You are missing the **Kick Members** permission')
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('Missing Required Arguments.\n**Example**\nC.kick <@716138613783527505> (reason optional)')


@client.command(aliases=['Ban', 'BAn', 'BAN'])
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, reason=None):
   await member.ban(reason=reason)
   await ctx.channel.purge(limit=1)
   channel = client.get_channel(716124863839993886)
   await channel.purge(limit=1)
   await ctx.send(f'Banned {member} for {reason}\n{member.mention}')
   embed = discord.Embed(
       title=f"Banned {member.name}#{member.discriminar}",
       description=f'Banned for {reason}',
       colour=discord.Colour.red()
   )
   embed.set_author(name=f'{member.name}#{member.discriminator}', icon_url=member.avatar_url)
   await channel.send(embed=embed)


@ban.error
async def ban_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send('You are missing the **Ban Members** permission')
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('Missing Required Arguments.\n**Example**\nC.ban <@716138613783527505> (reason optional)')


@client.command(aliases=['Unban', 'UNban', 'UNBan', 'UNBAn', 'UNBAN'])
@commands.has_permissions(ban_members=True)
async def unban(ctx, *, member):
   banned_users = await ctx.guild.bans()
   member_name, member_discriminator = member.split('#')
   for ban_entry in banned_users:
       user = ban_entry.user
       if (user.name, user.discriminator) == (member_name, member_discriminator):
           await ctx.guild.unban(user)
           await ctx.send(f'Unbanned {user.name}#{user.discriminator}')
           return


@unban.error
async def unban_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send('You are missing the **Ban Members** permission')
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('Missing Required Arguments.\n**Example**\nC.unban <@716138613783527505>')


@client.command(aliases=['Help', 'HElp', 'HELp', 'HELP'])
async def help(ctx):
    author = ctx.message.author
    embed = discord.Embed(
        title='Commands for the Bot',
        description=f'Hello {author} here is the list of commands that the bot has!',
        colour=discord.Colour.blue()
        )
    embed.set_footer(text='Bot made by some dumb kid.')
    embed.add_field(name='Kick', value='Kicks the mentioned user.\n**Example:**\nC.kick <@716138613783527505>', inline=False)
    embed.add_field(name='Ban', value='Bans the mentioned user.\n**Example**\nC.ban <@716138613783527505>', inline=True)
    embed.add_field(name='Unban', value='Unbans the user specified\n**Example**\nC.unban TheCatKingdom#3761', inline=True)
    embed.add_field(name='Purge/Clear', value='Deletes a specified amount of messages.\n**Example**\nC.purge 10', inline=False)
    embed.add_field(name='Ping', value='Checks the latency to the server.', inline=False)
    embed.add_field(name='DisRules(Comming soon...)', value='Sends the rules of the server.(Discord)', inline=True)
    embed.add_field(name='SerRules(Comming soon...)', value='Sends the rules of the server.(Server)', inline=True)
    await ctx.send(f"Check Your Dm's {author}!")
    await author.send(embed=embed)


client.run(os.environ['TOKEN'])
