"""IsharMUD Discord bot"""
import interactions
import discord_secret
from database import db_session
from helptab import search_help_topics
from models import Challenge, Player, Season

bot = interactions.Client(token=discord_secret.TOKEN, default_scope=discord_secret.GUILD)


@bot.command()
async def challenges(ctx: interactions.CommandContext):
    """Show the current in-game Ishar MUD challenges"""
    completed = 0
    all_challenges = Challenge.query.filter_by(is_active=1).all()
    for challenge in all_challenges:
        if challenge.winner_desc != '':
            completed = completed + 1
    await ctx.send(f'There are currently {completed} completed / {len(all_challenges)} total challenges!')
    db_session.close()


@bot.command()
async def deadhead(ctx: interactions.CommandContext):
    """Show the player with the most in-game deaths"""
    deadman = Player.query.filter_by(is_deleted=0, game_type=0).order_by(-Player.deaths).first()
    await ctx.send(f'The player who has died most is: {deadman.name} - {deadman.deaths} times!')
    db_session.close()


@bot.command(
    name="say_something",
    description="say something!",
    options = [
        interactions.Option(
            name="text",
            description="What you want to say",
            type=interactions.OptionType.STRING,
            required=True,
        )
    ]
)
async def my_first_command(ctx: interactions.CommandContext, text: str):
    """This is my first command"""
    await ctx.send(f"You said '{text}'!")


@bot.command()
async def mudhelp(ctx: interactions.CommandContext, search=None):
    """Search for MUD help"""
    search_topics = search_help_topics(all_topics=None, search=search)
    if not search_topics:
        await ctx.send('Sorry, but there were no search results.')
    elif len(search_topics) == 1:
        found_topic = next(iter(search_topics.values()))
        topic_name = found_topic['name']
        topic_url = f"isharmud.com/help/{topic_name}".replace(' ', '%20')
        await ctx.send(f'{topic_name}: {topic_url}')
    elif len(search_topics) > 1:
        search_url = f"isharmud.com/help/{search}".replace(' ', '%20')
        await ctx.send(f'{search_url}')


@bot.command()
async def season(ctx: interactions.CommandContext):
    """Show the current Ishar MUD season"""
    current_season = Season.query.filter_by(is_active=1).order_by(-Season.season_id).first()
    await ctx.send(f'It is currently Season {current_season.season_id} which ends in {current_season.expires}!')
    db_session.close()


bot.start()
