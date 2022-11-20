"""
Discord bot simply runs in a screen session, for now
So far, there are only two "slash commands" (/):
/season and /challenges
"""
import interactions
import discord_secret
from database import db_session
from models import Challenge, Player, Season

bot = interactions.Client(token=discord_secret.TOKEN, default_scope=discord_secret.GUILD)


@bot.command()
async def season(ctx: interactions.CommandContext):
    """Show the current Ishar MUD season information"""
    current_season  = Season.query.filter_by(is_active=1).order_by(-Season.season_id).first()
    await ctx.send(
        f'It is currently Season {current_season.season_id}, ' \
        f'which ends in {current_season.expires}.'
    )
    db_session.close()


@bot.command()
async def challenges(ctx: interactions.CommandContext):
    """Show the current in-game Ishar MUD challenges"""
    current_challenges  = Challenge.query.filter_by(is_active=1).order_by(
                            Challenge.adj_level,
                            Challenge.adj_people
                        ).all()
    count       = len(current_challenges)
    completed   = 0
    for challenge in current_challenges:
        if challenge.winner_desc != '':
            completed   = completed + 1
    await ctx.send(f"Challenges: {completed} completed / {count} total")
    db_session.close()


@bot.command()
async def deadhead(ctx: interactions.CommandContext):
    """Show the name and count of player with the most deaths"""
    deadman = Player.query.filter_by(is_deleted=0,game_type=0).order_by(-Player.deaths).first()
    await ctx.send(f"The player who has died most is: {deadman.name} - {deadman.deaths} times!")
    db_session.close()


bot.start()
