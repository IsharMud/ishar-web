import filters
import datetime
import discord_secret
import interactions
import models

"""
Testing Discord Bot here
"""
guild   = '636680767921061909'
bot     = interactions.Client(token=discord_secret.token, default_scope=guild)

@bot.command()
async def season(ctx: interactions.CommandContext):
    """Show the current Ishar MUD season information"""
    season  = models.Season.query.filter_by(is_active = 1).first()
    print(season)
    end_dt = filters.unix2datetime(season.expiration_date)
    diff_dt = end_dt - datetime.datetime.today()
    what = 'day'
    if diff_dt.days != 1:
        what += 's'
    await ctx.send(f"It is currently Season {season.season_id}, which ends in {diff_dt.days} {what}, on {end_dt.strftime('%A, %B %d, %Y')}!")


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
    await ctx.send(f"There are currently {count} challenges, and {completed} completed.")


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
        msg = f"There are currently {count} users online: {online}"
    else:
        msg = 'Unfortunately, nobody is online right now.'

    await ctx.send(msg)

bot.start()
