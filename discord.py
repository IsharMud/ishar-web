"""IsharMUD Discord bot"""
import re
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


@bot.command(name='mudhelp', description='Find Ishar MUD help topic',
    options = [
        interactions.Option(name='search', description='title of a help topic to search for',
            type=interactions.OptionType.STRING, required=True)
    ]
)
async def mudhelp(ctx: interactions.CommandContext, search: str):
    """Search for MUD help"""
    ephemeral = False

    # Try to find any help topics containing the search term
    search_topics = search_help_topics(all_topics=None, search=search)

    # Say so, only to that user, if there were no results
    if not search_topics:
        out = 'Sorry, but there were no search results.'
        ephemeral = True

    # Link single search result, and if there is only one
    elif len(search_topics) == 1:
        found_topic = next(iter(search_topics.values()))

        # Show the topic name and link
        topic_name = found_topic['name']
        topic_url = f'https://isharmud.com/help/{topic_name}'.replace(' ', '%20')
        out = f'{topic_name}: {topic_url}\n'

        # Show any specific items within the help topic
        for item_type in ['syntax', 'minimum', 'level', 'class']:
            if item_type in found_topic:
                found_topic[item_type] = re.sub('<[^<]+?>', '', found_topic[item_type]).replace('&gt;', '>').replace('&lt;', '<').replace('&quot;', '"')
                if found_topic[item_type].strip() != '':
                    out += f'> {item_type.title()}: {found_topic[item_type].strip()}\n'

        # Show the first 100 lines of the help topic body text
        topic_body = found_topic['body_text'].replace('&gt;', '>').replace('&lt;', '<').replace('&quot;', '"')
        if len(topic_body) > 100:
            body_begin = topic_body[0:100] + '...'
        else:
            body_begin = topic_body
        out += body_begin

    # Link search results, if there are multiple results
    elif len(search_topics) > 1:
        search_url = f'<https://isharmud.com/help/{search}>'.replace(' ', '%20')
        out = f'Search Results: {search_url}'

    # Send the help search response
    await ctx.send(out, ephemeral=ephemeral)

    db_session.close()


@bot.command()
async def season(ctx: interactions.CommandContext):
    """Show the current Ishar MUD season"""
    current_season = Season.query.filter_by(is_active=1).order_by(-Season.season_id).first()
    await ctx.send(f'It is currently Season {current_season.season_id} which ends in {current_season.expires}!')
    db_session.close()


@bot.command()
async def faq(ctx: interactions.CommandContext):
    """Link to the Frequently Asked Questions page"""
    await ctx.send('https://isharmud.com/faq')

@bot.command()
async def faqs(ctx: interactions.CommandContext):
    """Link to the Frequently Asked Questions page"""
    await ctx.send('https://isharmud.com/faq')


@bot.command()
async def get_started(ctx: interactions.CommandContext):
    """Link to the Getting Started page"""
    await ctx.send('https://isharmud.com/get_started')

@bot.command()
async def getstarted(ctx: interactions.CommandContext):
    """Link to the Getting Started page"""
    await ctx.send('https://isharmud.com/get_started')


bot.start()
