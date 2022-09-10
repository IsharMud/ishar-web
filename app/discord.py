import datetime
import discord_secret
import interactions
import models

"""
Discord bot simply runs in a screen session, for now
So far, there are only three "slash commands" (/):
/season, /challenges, and /who
"""

guild   = '636680767921061909'
bot     = interactions.Client(token=discord_secret.token, default_scope=guild)

@bot.command()
async def season(ctx: interactions.CommandContext):
    """Show the current Ishar MUD season information"""
    season  = models.Season.query.filter_by(is_active = 1).first()
    print(season)
    await ctx.send(f"It is currently Season {season.season_id}, which ends in {season.expires_in}, on {season.expiration_dt.strftime('%A, %B %d, %Y')}!")


@bot.command()
async def challenges(ctx: interactions.CommandContext):
    """Show the current in-game Ishar MUD challenges"""
    challenges  = models.Challenge.query.filter_by(is_active = 1).order_by(
                    models.Challenge.adj_level,
                    models.Challenge.adj_people
                ).all()
    print(challenges)
    count       = len(challenges)
    completed   = 0
    for challenge in challenges:
        if challenge.winner_desc != '':
            completed = completed + 1
    await ctx.send(f"Challenges: {completed} completed / {challenges} total")


@bot.command()
async def who(ctx: interactions.CommandContext):
    """Show the current in-game list of users online"""
    who = models.Player.query.filter(
        models.Player.logon >= models.Player.logout
    ).order_by(
        -models.Player.true_level,
        -models.Player.remorts,
        models.Player.name
    ).all()
    print(who)
    count   = len(who)
    if count > 0:
        names   = [p.name for p in who]
        print('names: ', names)
        online  = ', '.join(names)
        print('online: ', online)
        what    = 'player'
        if count != 1:
            what += 's'
        msg = f"There are currently {count} {what} online: {online}"
    else:
        msg = 'Unfortunately, nobody is online right now.'

    await ctx.send(msg)

bot.start()
