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


@tasks.loop(seconds=30)
async def change_status():
   await client.change_presence(activity=discord.Game(next(status)))


@client.event
async def on_member_join(user):
    print(f'{user.name}#{user.discriminator} joined the server')
    embed = discord.Embed(
        title='Welcome to TheCatKingdom!',
        description=f'Hello {user}! Welcome to the Discord Server!',
        colour=discord.Colour.green()
    )
    embed.set_author(name=f'{user.name}#{user.discriminator}', icon_url=user.avatar_url)
    channel = client.get_channel(709523289109823570)
    await channel.send(embed=embed)


@client.event
async def on_member_remove(user):
    embed = discord.Embed(
        title="Its sad to see you go:'(",
        description=f'Goodbye {user.name}#{user.discriminator}, we hope to see you again!',
        colour=discord.Colour.red()
    )
    embed.set_author(name=f'{user.name}#{user.discriminator}', icon_url=user.avatar_url)
    channel = client.get_channel(709523289109823570)
    await channel.send(embed=embed)


@client.command()
async def ping(ctx):
    await ctx.send(f'Pong!\n**Latency**: {round(client.latency*1000)}ms')


# Embed Example
#    embed = discord.Embed(
#       title='Title',
#       description='Description Text',
#       colour=discord.Colour.blue()
#   )
#
#   embed.set_footer(icon_url='Url', text='Footer Text')
#   embed.set_image(url='Url')
#   embed.set_thumbnail(url='Url')
#   embed.set_author(name="Authors Name", icon_url='Url')
#   embed.add_field(name='Field Name', value='Field Value', inline=True)
#   embed.add_field(name='Field Name', value='Field Value', inline=True)
#   embed.add_field(name='Field Name', value='Field Value', inline=True)
#   await ctx.send(embed=embed)


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
   if isinstance(error, commands.MissingRequiredArgument):
       await ctx.send('**Command**:\n`b.clear #`\n                  ^\n**Missing Value**')
   elif isinstance(error, commands.MissingPermissions):
       await ctx.send('**Command**:\nMissing Manage Messages permission')


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
   if isinstance(error, commands.MissingRequiredArgument):
       await ctx.send('**Command**:\n`b.purge #`\n                  ^\n**Missing Value**')
   elif isinstance(error, commands.MissingPermissions):
       await ctx.send('**Command**:\nMissing manage messages permission')


@client.command(aliases=['Kick', 'KICK', 'KIck', 'KICk'])
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, *, reason=None):
    await member.kick(reason=reason)
    await ctx.channel.purge(limit=1)
    channel = client.get_channel(709523289109823570)
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
        await ctx.send('Missing Required Arguments')


@client.command(aliases=['Ban', 'BAn', 'BAN'])
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, reason=None):
   await member.ban(reason=reason)
   await ctx.channel.purge(limit=1)
   await ctx.send(f'Banned {discord.Member}')


@ban.error
async def ban_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send('You are missing the **Ban Members** permission')
    elif isinstance(error, commands.MissingPermissions):
        await ctx.send('Missing Required Arguments')


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
async def ban_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send('You are missing the **Ban Members** permission')
    elif isinstance(error, commands.MissingPermissions):
        await ctx.send('Missing Required Arguments')


@client.command(aliases=['Help', 'HElp', 'HELp', 'HELP'])
async def help(ctx):
    embed = discord.Embed(
        title='Title',
        description='Description Text',
        colour=discord.Colour.blue()
        )
    embed.set_thumbnail(url='Url')
    embed.set_author(name="Authors Name", icon_url='Url')
    embed.add_field(name='Field Name', value='Field Value', inline=True)
    embed.add_field(name='Field Name', value='Field Value', inline=True)
    embed.add_field(name='Field Name', value='Field Value', inline=True)
    await ctx.send(embed=embed)

client.run(os.environ['TOKEN'])
