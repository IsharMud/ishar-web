"""IsharMUD Discord bot"""
import re
from io import StringIO
import interactions
import discord
import discord_secret
from database import db_session
from helptab import search_help_topics, search_help_spells
from models import Challenge, Player, Season


def get_single_help(topic=None):
    """Return extended output for a single help topic"""
    # Get the single topic name and link
    topic_url = f"<https://isharmud.com/help/{topic['name']}>".replace(' ', '%20')
    out = f"{topic['name']}: {topic_url}\n"

    # Get any specific items within the help topic
    for item_type in ['syntax', 'minimum', 'class', 'level']:
        if item_type in topic:
            topic[item_type] = re.sub('<[^<]+?>', '', topic[item_type]).replace('&gt;', '>').replace('&lt;', '<').replace('&quot;', '"')
            if topic[item_type].strip() != '':
                out += f'> {item_type.title()}: {topic[item_type].strip()}\n'

    # Return the help topic without HTML in the pre-formatted body text
    topic_body = re.sub('<[^<]+?>', '', topic['body_text'])
    topic_body = topic_body.replace('&gt;', '>').replace('&lt;', '<').replace('&quot;', '"')
    out += f'```{topic_body}```'
    return out


# Connect/authenticate the IsharMUD Discord bot
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
    """Search for MUD help topics"""
    ephemeral = False

    # Try to find any help topics containing the search term
    search_topics = search_help_topics(all_topics=None, search=search)

    # Say so, only to that user, if there were no results
    if not search_topics:
        out = 'Sorry, but there were no search results.'
        ephemeral = True

    # Get single search result, if there is only one
    elif len(search_topics) == 1:
        found_topic = next(iter(search_topics.values()))
        out = get_single_help(topic=found_topic)

    # Link search results, if there are multiple results
    elif len(search_topics) > 1:
        search_url = f'<https://isharmud.com/help/{search}>'.replace(' ', '%20')
        out = f'Search Results: {search_url} ({len(search_topics)} topics)'

    # Send the help search response
    await ctx.send(out, ephemeral=ephemeral)

    db_session.close()


@bot.command(name='spell', description='Find Ishar MUD spell help',
    options = [
        interactions.Option(name='search', description='name of a spell to search for',
            type=interactions.OptionType.STRING, required=True)
    ]
)
async def spell(ctx: interactions.CommandContext, search: str):
    """Search for MUD help topics"""
    ephemeral = False

    # Try to find any spell help topics containing the search term
    search_spells = search_help_spells(all_topics=None, spell=search)

    # Say so, only to that user, if there were no results
    if not search_spells:
        out = 'Sorry, but no such spell could be found!'
        ephemeral = True

    # Get single spell search result, if there is only one
    elif len(search_spells) == 1:
        found_spell = next(iter(search_spells.values()))
        out = get_single_help(topic=found_spell)

    # Link search results, if there are multiple results
    elif len(search_spells) > 1:
        spell_search_url = f'<https://isharmud.com/help/Spell%20{spell}>'.replace(' ', '%20')
        out = f'Spell Results: {spell_search_url} ({len(search_spells)} spells)'

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
