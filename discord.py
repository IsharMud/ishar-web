"""
Discord bot simply runs in a screen session, for now
So far, there are only two "slash commands" (/):
/season and /challenges
"""
import interactions
import discord_secret
import models

bot = interactions.Client(token=discord_secret.TOKEN, default_scope=discord_secret.GUILD)

@bot.command()
async def season(ctx: interactions.CommandContext):
    """Show the current Ishar MUD season information"""
    current_season  = models.Season.query.filter_by(is_active = 1).first()
    await ctx.send(
        f'It is currently Season {current_season.season_id}, ' \
        f'which ends in {current_season.expires}, on ' \
        f"{current_season.expiration_dt.strftime('%A, %B %d, %Y')}!"
    )

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

bot.start()
