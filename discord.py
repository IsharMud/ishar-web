"""
Discord bot simply runs in a screen session, for now
So far, there are only two "slash commands" (/):
/season and /challenges
"""
import interactions
import sentry_sdk
import discord_secret
from database import db_session
import models
import sentry_secret
from dateutil.relativedelta import relativedelta
from datetime import datetime


sentry_sdk.init(dsn=sentry_secret.DSN, traces_sample_rate=1.0)

bot = interactions.Client(token=discord_secret.TOKEN, default_scope=discord_secret.GUILD)

@bot.command()
async def season(ctx: interactions.CommandContext):
    """Show the current Ishar MUD season information"""
    current_season  = models.Season.query.filter_by(is_active = 1).first()
    start_time = datetime.utcnow()
    end_time = current_season.expiration_date
    diff = relativedelta(start_time, end_time)
    diff_str = ""
    if (diff.months > 0):
        diff_str += "%d months, " % (diff.months)
    
    diff_str += "%d days , and %d hours" % (diff.days, diff.hours)
    await ctx.send(
        f'It is currently Season {current_season.season_id}, ' \
        f'which ends in {current_season.expires}, on ' \
        f"{diff_str}!"
    )
    db_session.close()

@bot.command()
async def challenges(ctx: interactions.CommandContext):
    """Show the current in-game Ishar MUD challenges"""
    current_challenges  = models.Challenge.query.filter_by(is_active = 1).order_by(
                            models.Challenge.adj_level,
                            models.Challenge.adj_people
                        ).all()
    count       = len(current_challenges)
    completed   = 0
    for challenge in current_challenges:
        if challenge.winner_desc != '':
            completed   = completed + 1
    await ctx.send(f"Challenges: {completed} completed / {count} total")
    db_session.close()

bot.start()
