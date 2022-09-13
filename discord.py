"""
Discord bot simply runs in a screen session, for now
So far, there are only three "slash commands" (/):
/season, /challenges, and /who
"""
import discord_secret
import interactions
import models

bot     = interactions.Client(token=discord_secret.TOKEN, default_scope=discord_secret.GUILD)

@bot.command()
async def season(ctx: interactions.CommandContext):
    """Show the current Ishar MUD season information"""
    season  = models.Season.query.filter_by(is_active = 1).first()
    print(season)
    await ctx.send(f"It is currently Season {season.season_id}, which ends in {season.expires}, on {season.expiration_dt.strftime('%A, %B %d, %Y')}!")


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
    await ctx.send(f"Challenges: {completed} completed / {count} total")

bot.start()
