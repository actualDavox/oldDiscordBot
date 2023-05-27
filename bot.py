import discord
from discord.ext import commands
from itertools import cycle
import asyncio
import datetime
import praw
from random import randint
import random
import time


client = commands.Bot(command_prefix='.')
TOKEN = 'Nzg4NzgxMTEwMTc1NTk2NjI1.X9ofpw.RZuTpNLpUKudUNZyonOerJQwIE4'
client.remove_command('help')


@client.event
async def on_ready():
    print(
    f'{client.user.name} is now running in {len(client.guilds)} servers.')


async def change_status():
    await client.wait_until_ready()
    status = [f'in {len(client.guilds)} servers!', 'Type $help!']
    msgs = cycle(status)
    while not client.is_closed():
        current_status = next(msgs)
        await client.change_presence(
        game=discord.Game(name=current_status, type=1))
        await asyncio.sleep(60)


@client.event
async def on_member_join(ctx, member: discord.User):
    channel = discord.utils.get(
    client.server.channels, f'📊Member count: {member.server.member_count}')
    await ctx.send(f'Hey {member.mention}, and welcome to {member.server}.')
    await client.edit_channel(
    member.bot.myattribute,
    name=f"📊Member count: {member.server.member_count}")


@client.event
async def on_member_remove(member: discord.User):
await ctx.send(f'{member.user.name} left us.')
    channel = discord.utils.get(
        client.server.channels, f'📊Member count: {member.server.member_count}')
    await client.edit_channel(
        channel, name=f"📊Member count: {member.server.member_count+1}")


@client.command(pass_context=True)
async def check(ctx):
    if ctx.message.author.server_permissions.administrator:
        list1 = []
        for x in client.get_all_members():
            list1.append(x.name)
        await ctx.send(list1)

@client.command(pass_context=True)
async def help(ctx, page=None):
    if page is None:
        await ctx.send(
            '**Correct usage:** $help {page}\nPage 1: Staff commands\nPage 2: Misc commands'
        )
    elif page == '1':
        help_embed1 = discord.Embed(
        title='Help page [1]',
        description='Note: All the commands below require kick / ban permissions. Normal users won\'t be able to execute any of them.',
        colour=0x11bf1c)
        help_embed1.add_field(
        name='$nick <user> <new nickname>',
        value='$nick @username#ID Nick',
        inline=False)
        help_embed1.add_field(
        name='$purge <amount of messages - Optional (default set to 100) >',
        value='$purge 100',
        inline=False)
        help_embed1.add_field(
        name='$warn <user> <reason - Optional>',
        value='$warn @username#ID', 
        inline=False)
        help_embed1.add_field(
        name='$kick <user> <reason - Optional>',
        value='$kick @username#ID',
        inline=False
        )
        help_embed1.add_field(
        name='$mute <user> <reason - Optional>',
        value='.mute',
        inline=False)
        help_embed1.add_field(
        name='$unmute <user> <reason - Optional>',
        value='',
        inline=False)
        help_embed1.add_field(
        name='$ban <user> <reason - Optional>',
        inline=False)
        help_embed1.add_field(
        name='$role <user> <role>',
        inline=False)
        help_embed1.add_field(
        name='$unrole <user> <role>',
        inline=False)
        help_embed1.timestamp = datetime.datetime.utcnow()

        await ctx.send(ctx.message.author, embed=help_embed1)
        await ctx.send(
        f"{ctx.message.author.mention}, I sent you a message with the help page you requested."
    )
    elif page == '2':
        help_embed2 = discord.Embed(
        title='Help page [2]',
        description=
        'Most of those commands can be used with any specific permissions.',
        color=0x11bf1c)
        help_embed2.add_field(
        name='$info <user>', value=' ', inline=False)
        help_embed2.add_field(
        name='$ping', value='Returns the bot\'s ping.', inline=False)
        help_embed2.add_field(
        name='$meme {subreddit}',
        value=
        'Returns a trending post in the subreddit given. Default one is set to /r/darkmemes **Note:** You can only chose the subreddit in the channel "#fordaboiiiis".',
        inline=False)
        help_embed2.add_field(
        name='$report {problem}',
        value='$report This is a random problem',
        inline=False)
        help_embed2.add_field(
        name='$suggest {suggestion}',
        value='$suggest This is a suggestion',
        inline=False)
        help_embed2.add_field(
        name='$update',
        value=
        'This command updates the member count. It should always automatically update when the bot is online and someone joins/leaves.',
        inline=False)
        help_embed2.add_field(
        name='$invite',
        value=
        f'This command returns a link to invite {client.user.name} to your server. ',
        inline=False)
        help_embed2.timestamp = datetime.datetime.utcnow()
        await ctx.send(ctx.message.author, embed=help_embed2)
        await ctx.send(
        f'{ctx.message.author.mention}, I sent you a message with the help page requested. '
    )
    else:
        await ctx.send(
        "**Correct usage:** $help {page}\nPage 1: Staff commands\nPage 2: Misc commands"
    )


@client.command(pass_context=True)
async def role(ctx, user: discord.Member = None, role=None):
    try:
        if ctx.message.author.server_permissions.administrator:
            if role is not None and user is not None:
                if discord.utils.get(
                    ctx.message.server.roles, name=role.lower()):
                    role = discord.utils.get(
                    ctx.message.server.roles, name=role.lower())
                    await client.add_roles(user, role)
                    await ctx.send(f"{user.name} has received **{role}**.")
                else:
                    await ctx.send("Role not found")
            else:
                await ctx.send('**Correct usage:** $role {user} {role}')
        else:
            await ctx.send(
            "You do not have the permissions required to execute this command.")
    except discord.DiscordException as e:
        await ctx.send("Please report the issue to me using ``$report [problem]``\nProviding the error code given below will make things a lot easier.\n**Error code: {}** "
        .format(e))


@client.command(pass_context=True)
async def unrole(ctx, user: discord.Member = None, *, role=None):
    try:
        if ctx.message.author.server_permissions.administrator:
            if role is not None and user is not None:
                if discord.utils.get(
                    ctx.message.server.roles, name=role.lower()):
                    role = discord.utils.get(
                    ctx.message.server.roles, name=role.lower())
                    await client.remove_roles(user, role)
                    await ctx.send(f"{user.name} has lost **{role}**.")
                else:
                    await ctx.send("Role not found")
            else:
                await ctx.send('**Correct usage:** $unrole {user} {role}')
        else:
            await ctx.send(
            "You do not have enough permissions to execute this command.")
    except discord.DiscordException as e:
        await ctx.send("Please report the issue to me using ``$report [problem]``\nProviding the error code given below will make things a lot easier.\n**Error code: {}** "
        .format(e))


@client.command(pass_context=True)
async def nick(ctx, user: discord.Member = None, new_nick=None):
    if new_nick is None and user is None or user is None or new_nick is None:
        await ctx.send('**Correct usage:** $nick {new nick}')
    else:
        if ctx.message.author.server_permissions.kick_members:
            if new_nick.capitalize() == 'Reset':
                await client.change_nickname(user, None)
                await ctx.send(f"{user.mention}\'s nick has been reset.")
            else:
                await client.change_nickname(user, new_nick)
                await ctx.send(f"{user.mention}'s nick has been changed to **{new_nick}**.")
        else:
            await ctx.send(
            'You do not have the permissions required to execute this command.')


@client.command(pass_context=True)
async def dice(ctx, sides=None, amount=1):
    dice_embed = discord.Embed(
    title=
    'You need to provide the amount of sides & the amount of dices to roll.',
    description=
    'Example: .dice 10 (amount of sides) 5 (amount of dices to roll)\nSupported amount of dices: 1, 2, 3, 5, 10, 20',
    colour=discord.Colour.green())
    if sides is None and amount is not None:
        await ctx.send(embed=dice_embed)
    if sides is not None and amount is not None:
        if amount == 1:
            await ctx.send('Number given: ``{}``'.format((randint(
            1, int(sides)))))
        elif amount == 2:
            await ctx.send('Numbers given: ``{}`` & ``{}``'.format(
            randint(1, int(sides)), randint(1, int(sides))))
        elif amount == 3:
            await ctx.send('Numbers given: ``{}``, ``{}`` & ``{}``'.format(
            randint(1, int(sides)), randint(1, int(sides)),
            randint(1, int(sides))))
        elif amount == 5:
            await ctx.send(
            'Numbers given: ``{}``, ``{}``, ``{}``, ``{}`` & ``{}``'.
            format(
                randint(1, int(sides)), randint(1, int(sides)),
                randint(1, int(sides)), randint(1, int(sides)),
                randint(1, int(sides))))
        elif amount == 10:
            await ctx.send(
            'Numbers given: ``{}``, ``{}``, ``{}``, ``{}``, ``{}``, ``{}``, ``{}``, ``{}``, ``{}`` & ``{}``'
            .format(
                randint(1, int(sides)), randint(1, int(sides)),
                randint(1, int(sides)), randint(1, int(sides)),
                randint(1, int(sides)), randint(1, int(sides)),
                randint(1, int(sides)), randint(1, int(sides)),
                randint(1, int(sides)), randint(1, int(sides))))
        elif amount == 20:
            await ctx.send(
            'Numbers given: ``{}``, ``{}``, ``{}``, ``{}``, ``{}``, ``{}``, ``{}``, ``{}``, ``{}``, ``{}``, ``{}``, ``{}``, ``{}``, ``{}``, ``{}``, ``{}``, ``{}``, ``{}``, ``{}`` & ``{}``'
            .format(
                randint(1, int(sides)), randint(1, int(sides)),
                randint(1, int(sides)), randint(1, int(sides)),
                randint(1, int(sides)), randint(1, int(sides)),
                randint(1, int(sides)), randint(1, int(sides)),
                randint(1, int(sides)), randint(1, int(sides)),
                randint(1, int(sides)), randint(1, int(sides)),
                randint(1, int(sides)), randint(1, int(sides)),
                randint(1, int(sides)), randint(1, int(sides)),
                randint(1, int(sides)), randint(1, int(sides)),
                randint(1, int(sides)), randint(1, int(sides))))
        else:
            await ctx.send("Invalid amount.")
            await ctx.send(embed=dice_embed)
    else:
        await ctx.send('Invalid command.\n**Correct usage:**-dice 6 10')


@client.command(pass_context=True)
async def info(ctx, user: discord.Member = None):
    if user is None:
        await ctx.send("**Correct usage:** -info {mention}")
    else:
        info_embed = discord.Embed(
        title=f"{user.name}'s information.", color=discord.Colour.orange())
        info_embed.add_field(
        name='**Account created at:**',
        value=user.created_at.strftime('%d-%m-%y'),
        inline=True)
        info_embed.add_field(
        name='**Current status:**', value=user.status, inline=True)
        info_embed.add_field(
        name='**Highest user\'s role on this server:**',
        value="{}".format(user.top_role.mention),
        inline=True)
        info_embed.add_field(
        name='**Joined at:**',
        value='{}'.format(user.joined_at.strftime('%d-%m-%y ')),
        inline=True)
        info_embed.add_field(name='**Name:**', value=user.name, inline=True)
        info_embed.add_field(name='**Avatar:**', value='\u200b', inline=True)
        info_embed.timestamp = datetime.datetime.utcnow()
        info_embed.set_footer(text=" | User ID: {}".format(user.id))
        info_embed.set_image(url=user.avatar_url)
        await ctx.send(embed=info_embed)


@client.command(pass_context=True)
async def ping(ctx):
    t = await ctx.send('Pong!')
    ms = (t.timestamp - ctx.message.timestamp).total_seconds() * 1000
    await client.edit_message(
    t, new_content='Pong!\n:timer_clock:``{}ms``'.format(int(ms)))


@client.command(pass_context=True)
async def ban(ctx, user: discord.Member = None, *, reason=None):
    try:
        if ctx.message.author.server_permissions.ban_members:
            if user is None and reason is None:
                await ctx.send(
                "**Correct usage:** $ban {user} {reason}\n**Note:** The reason is optional."
            )
            elif user is not None and reason is not None:
                await client.ban(user, delete_message_days=14)
                await ctx.send(
                user,
                f'You have been banned in **{ctx.message.server}**.\nReason: {reason}'
            )
                await ctx.send(f"**{user}** has been banned succesfully.")
            elif user is not None and reason is None:
                await client.ban(user, delete_message_days=14)
                await ctx.send(
                user,
                f'You have been banned in **{ctx.message.server}**.\n**Reason:** None given. '
            )
        else:
            await ctx.send(
            "You do not have the permissions required to execute this command.")
    except Exception as e:
        await ctx.send("Please report the issue to me using ``$report [problem]``\nProviding the error code given below will make things a lot easier.\n**Error code: {}** "
        .format(e))


@client.command(pass_context=True)
async def unban(ctx, user: discord.Member = None, *, reason=None):
    if ctx.message.author.server_permissions.ban_members:
        if user is None and reason is None:
            await ctx.send(
                "**Correct usage:** $unban {user} {reason}\n**Note:** Reason is optional."
        )
        elif user is not None and reason is not None:
            a = await client.get_bans(ctx.message.server)
            if user in a:
                await client.unban(ctx.message.server, discord.Object(user.id))
                await ctx.send(
                user,
                f'You have been unbanned of {ctx.message.server}.\n**Reason:** {reason}'
            )
                await ctx.send(f"{user} has been unbanned succesfully.")
            else:
                await ctx.send(f"{user} is currently not banned.")
        elif user is not None and reason is None:
            try:
                await client.unban(ctx.message.server, discord.Object(user.id))
                await ctx.send(
                user,
                f'You have been unbanned of {ctx.message.server}.\n**Reason:** None given.'
            )
                await ctx.send(f"{user} has been unbanned succesfully.")
            except discord.HTTPException:
                await ctx.send(f'{user.name} is currently not banned.')
    else:
        await ctx.send(
        'You do not have the permissions required to execute this command.')


@client.command(pass_context=True)
async def kick(ctx, user: discord.Member = None, *, reason=None):
    if ctx.message.author.server_permissions.kick_members:
        if user is None and reason is None:
            await ctx.send(
            "**Correct usage:** $kick {user} {reason}\n**Note:** Reason is optional."
        )
        elif user is not None and reason is not None:
            await client.kick(user)
            await ctx.send(f"{user} has been kicked succesfully.")
            await ctx.send(
            user,
            f'You have been kicked off {ctx.message.server}.\n**Reason:** {reason}'
        )
        elif user is not None and reason is None:
            await client.kick(user)
            await ctx.send(f"{user} has been kicked succesfully.")
            await ctx.send(
            user,
            f'You have been kicked off {ctx.message.server}.\n**Reason:** None given.'
        )
        else:
            await ctx.send("what the fuck")
    else:
        await ctx.send(
        'You do not have enough permissions to execute this command.')


@client.command(pass_context=True)
async def mute(ctx, user: discord.Member = None, *, reason=None):
    if not discord.utils.get(ctx.message.server.roles, name='Muted'):
        perms = discord.Permissions()
        perms.update(
        manage_roles=False,
        manage_messages=False,
        read_messages=True,
        read_message_history=True,
        send_messages=False,
        embed_links=False,
        change_nickname=False,
        add_reactions=False)
        await client.create_role(
        ctx.message.server,
        name='Muted',
        permissions=perms,
        colour=discord.Colour.red())
        muted = discord.utils.get(ctx.message.server.roles, name='Muted')
        if ctx.message.author.server_permissions.kick_members:
            if user is None and reason is None:
                await ctx.send(
            "**Correct usage:** $mute {user} {reason}\n**Note:** Reason is optional."
        )
            elif user is not None and reason is not None:
                await client.add_roles(user, muted)
                await ctx.send(
                    user,
                    f'You have been muted in {ctx.message.server}.\n**Reason:** None given.'
            )
            await ctx.send(f"{user} has been muted succesfully.")
        elif user is not None and reason is None:
            await client.add_roles(user, muted)
            await ctx.send(
            user,
            f'You have been muted in {ctx.message.server}.\n**Reason:** None given.'
            )
            await ctx.send(f"{user} has been muted succesfully.")
        else:
            await ctx.send("what the fuck")
    else:
        await ctx.send(
        'You do not have enough permissions to execute this command.')


@client.command(pass_context=True)
async def unmute(ctx, user: discord.Member = None, reason=None):
    role = discord.utils.get(ctx.message.server.roles, name='Muted')
    if ctx.message.author.server_permissions.ban_members:
        if not user.server_permissions.ban_members:
            if user is not None and reason is not None:
                if role in user.roles:
                    await client.remove_roles(user, role)
                    await ctx.send(f'{user.mention} was unmuted succesfully.'
                                    )
                else:
                    await ctx.send(f"{user.name} is not muted right now.")
            elif user is None and reason is None:
                await ctx.send(
                '**Correct usage:** $unmute {user} {reason}\n**Note:** Reason is optional.'
            )
            elif user is not None and reason is None:
                if role in user.roles:
                    await client.remove_roles(user, role)
                    await ctx.send(f"{user.mention} was unmuted."
                                    )
            else:
                await ctx.send(f'{user.name} is not muted right now.')
        else:
            await ctx.send(
            'Can not mute.'
        )
    else:
        await ctx.send(
        'You do not have the permissions required to execute this command.')


@client.command(pass_context=True)
async def purge(ctx, amount=None):
        if amount is None:
            await ctx.send('**Correct usage:** .purge {amount}')
        elif amount is not None:
            if int(amount) < 2000:
                await ctx.channel.purge(limit=int(amount))
                await ctx.send(
                '**{} messages** were deleted in **#{}**.'.format(
                    amount, ctx.message.channel))
                asyncio.sleep(3)
            else:
                await ctx.send(
                "You can only purge a maximum of 2000 messages at once.")
        else:
            await ctx.send(
            'You do not have enough permissions to execute this command.')


@client.command(pass_context=True)
async def warn(ctx, user: discord.Member = None, reason=None):
    if reason is not None and user is not None:
        if ctx.message.author.server_permissions.kick_members:
            if not user.server_permissions.kick_members:
                await ctx.send(
                user,
                f'You have been warned in {ctx.message.server}.\nReason: {reason}'
            )
                await ctx.send(f'{user.mention} has been warned succesfully.'
                                )
            else:
                await ctx.send(
                    'You can not warn this staff member, because he is a staff member.\n**Note:** Staff members are the users that can kick others.'
            )
        else:
            await ctx.send(
            "You do not have enough permissions to execute this command.")
    elif reason is None and user is None or reason is None:
        await ctx.send('**Correct usage:** $warn {user} {reason}')


@client.command(pass_context=True)
async def report(ctx, *, report=None):
    if report is None:
        await ctx.send('**Correct usage:** $report {the problem}')
    else:
        report_embed = discord.Embed(
        title='Report.',
        description=report,
        color=discord.Color.blue())
        report_embed.timestamp = datetime.datetime.utcnow()
        report_embed.set_author(
        name=ctx.message.author, icon_url=ctx.message.author.avatar_url)
        report_embed.add_field(
        name=
        f'Server: ``{ctx.message.server}``\nServer ID: ``{ctx.message.server.id}``',
        value='\u200b',
        inline=False)
        user = discord.utils.get(
        client.get_all_members(), id='398275702899605505')
        await ctx.send(user, embed=report_embed)
        await ctx.send(
        "Report has been send to the developer succesfully. :white_check_mark:"
    )


@client.command(pass_context=True)
async def suggest(ctx, suggestion=None):
    if suggestion is None:
        await ctx.send('**Correct usage:** $suggest {suggestion}')
    else:
        sug_embed = discord.Embed(
        title='Suggestion.',
        description=suggestion,
        color=discord.Color.blue())
        sug_embed.timestamp = datetime.datetime.utcnow()
        sug_embed.set_author(
        name=ctx.message.author, icon_url=ctx.message.author.avatar_url)
        sug_embed.add_field(
        name=
        f'Server: ``{ctx.message.server}``\nServer ID: ``{ctx.message.server.id}``',
        value='\u200b',
        inline=False)
        user = discord.utils.get(
        client.get_all_members(), id='398275702899605505')
        await ctx.send(user, embed=sug_embed)
        await ctx.send(
        "Suggestion has been send to the developer succesfully. :white_check_mark:"
    )


@client.command(pass_context=True)
async def invite(ctx):
    await ctx.send(
    f"Link to invite {client.user.name} to your server: \n<https://discordapp.com/api/oauth2/authorize?client_id=536976310942040064&permissions=8&scope=bot>\n**Note:** This link gives admin permissions to the bot. If you do not want the bot to have those permissions, you can remove the role he will receive as soon as he joins your server."
)


@client.command(pass_context=True)
async def r(ctx, *, sub=None):
    reddit = praw.Reddit(
    client_id='ya0KwwJ7kcxzKA',
    client_secret='xqEth1o8vLtJBYF6jK2ds_cDeSI',
    user_agent='android:com.example.myredditapp:v1.2.3 (by /u/yhacpy)')
#if not "\s" in sub:
    if not ctx.guild.id == "548653932386189354":
        if not ctx.guild.id == '548663240507392030' and sub is not None:
            memes_submissions = reddit.subreddit(sub).hot()
            post_to_pick = randint(1, 10)
            for i in range(0, post_to_pick):
                submission = next(
                    x for x in memes_submissions if not x.stickied)
            await ctx.send(submission.url)
        elif not ctx.guild.id == '548663240507392030' and sub is None:
            memes_submissions = reddit.subreddit('darkmemes').hot()
            post_to_pick = randint(1, 10)
            for i in range(0, post_to_pick):
                submission = next(
                    x for x in memes_submissions if not x.stickied)
            await ctx.send(submission.url)
        else:
            memes_submissions = reddit.subreddit('dankmemes').hot()
            post_to_pick = randint(1, 10)
            for i in range(0, post_to_pick):
                submission = next(
                    x for x in memes_submissions if not x.stickied)
            await ctx.send(submission.url)
    else:
            if sub is not None:
                memes_submissions = reddit.subreddit(sub).hot()
                post_to_pick = randint(1, 50)
                for i in range(0, post_to_pick):
                    submission = next(
                        x for x in memes_submissions if not x.stickied)
                await ctx.send(submission.url)
            else:
                memes_submissions = reddit.subreddit('dankmemes').hot()
                post_to_pick = randint(1, 1)
                for i in range(0, post_to_pick):
                    submission = next(
                        x for x in memes_submissions if not x.stickied)
                await ctx.send(submission.url)


@client.event
async def on_message_delete(message):
    channel3 = discord.utils.get(message.server.channels, name='logs')
    deleted = discord.Embed(
    color= discord.Colour.red()
    )
    deleted.add_field(name='Message sent by {} deleted in #{}.'.format(message.author, message.channel), value=message.content, inline=False)
    deleted.set_author(name=message.author, icon_url= message.author.avatar_url)
    deleted.timestamp = datetime.datetime.utcnow()
    deleted.set_footer(text='Message ID {}'.format(message.id))
    await ctx.send(channel3, embed=deleted)

@client.event
async def on_message_edit(before, after):
    if before.author.id != client.user.id:
    edited = discord.Embed(
        color = discord.Colour.orange()
    )
    edited.add_field(name='A message sent by {} was edited in #{}.'.format(before.author, before.channel), value='\u200b', inline=False)
    edited.add_field(name='Before:', value=before.content, inline=False)
    edited.add_field(name='After:', value=after.content, inline=False)
    edited.timestamp = datetime.datetime.utcnow()
    edited.set_footer(text='Message ID: {}'.format(before.id))
    edited.set_author(name=before.author, icon_url= before.author.avatar_url)
    channel = discord.utils.get(after.server.channels, name='logs')
    await ctx.send(channel, embed=edited)
    
    

    


@client.command(pass_context=True)
async def textcount(ctx, *, text=None):
    if text is not None:
        characters_no_space = len(text.replace(" ", ""))
        characters = len(text)
        words = len(text.split())
        embed = discord.Embed(
        description='**Text Statistics**', color=discord.Color.green())
        embed.add_field(
        name='\u200b',
        value=
        f'{words} words.\n{characters} characters.\n{characters_no_space} characters without spaces.',
        inline=False)
        time = datetime.datetime.utcnow()
        embed.timestamp = time
        await ctx.send(embed=embed)
    else:
        await ctx.send("**Correct usage:** $textcount [text]")


@client.event
async def on_message(ctx):
    await client.process_commands(ctx)


client.loop.create_task(change_status())
client.run(TOKEN)