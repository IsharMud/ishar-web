#!/usr/bin/python3
"""Ishar MUD Discord bot"""
import logging
import signal
import sys
import interactions
import discord_secret
from database import db_session
from helptab import search_help_topics
from models import Challenge, Player, Season

# Logging configuration
logging.basicConfig(level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    datefmt = '%Y-%m-%d %H:%M:%S %Z'
)


# Connect/authenticate Ishar MUD Discord bot
bot = interactions.Client(token=discord_secret.TOKEN, default_scope=discord_secret.GUILD)


def sigterm_handler(_signo, _stack_frame):
    """Try to handle SIGTERM gracefully"""
    sys.exit(0)


def get_single_help(topic=None):
    """Return extended output for a single help topic"""

    # Get the single topic name and link
    topic_url = f"<https://isharmud.com/help/{topic['name']}>".replace(' ', '%20')
    out = f"{topic['name']}: {topic_url}\n"

    # Get any specific items within the help topic
    for item_type in ['syntax', 'minimum', 'class', 'level']:
        if item_type in topic:
            if topic[item_type].strip() != '':
                out += f'> {item_type.title()}: {topic[item_type].strip()}\n'

    # Only return the name/link and specific items, if the body is too big
    out_wbody = f"{out}```{topic['body_text']}```"
    if len(out_wbody) > 2000:
        return out

    # Otherwise, return the whole body
    return out_wbody


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
    options = [interactions.Option(name='search', description='title of a help topic to search for',
        type=interactions.OptionType.STRING, required=True)])
async def mudhelp(ctx: interactions.CommandContext, search: str):
    """Search for MUD help topics"""

    # Try to find any help topics containing the search term
    ephemeral = True
    search_topics = search_help_topics(all_topics=None, search=search)

    # Tell user if there were no results
    if not search_topics:
        out = 'Sorry, but no such help topics could be found!'

    # Handle single search result, if there is only one
    elif len(search_topics) == 1:
        ephemeral = False
        found_topic = next(iter(search_topics.values()))
        out = get_single_help(topic=found_topic)

    # Link search results to user, if there are multiple results
    elif len(search_topics) > 1:
        search_url = f'<https://isharmud.com/help/{search}>'.replace(' ', '%20')
        out = f'Search Results: {search_url} ({len(search_topics)} topics)'

    # Send the help search response
    await ctx.send(out, ephemeral=ephemeral)
    db_session.close()


@bot.command(name='spell', description='Find Ishar MUD spell help',
    options = [interactions.Option(name='search', description='name of a spell to search for',
        type=interactions.OptionType.STRING, required=True)])
async def spell(ctx: interactions.CommandContext, search: str):
    """Search for spells in MUD help topics"""

    # Try to find any help topics containing the search term
    ephemeral = True
    search_results = search_help_topics(all_topics=None, search=search)

    # Narrow down the results to any topic named starting with "Spell "
    search_spell_results = {}
    for name, topic in search_results.items():
        if name.startswith('Spell '):
            search_spell_results[name] = topic

    # Get single spell search result, if there is only one
    if search_spell_results and len(search_spell_results) == 1:
        found_spell = next(iter(search_spell_results.values()))
        out = get_single_help(topic=found_spell)
        ephemeral = False

    # Handle multiple spell results
    elif len(search_spell_results) > 1:

        # Show user the matching spell names, if there were 10 or less
        #   Otherwise tell them to be more specific
        if len(search_spell_results) <= 10:
            out = f'Found {len(search_spell_results)} spells: {", ".join(search_spell_results.keys())}'
        else:
            out = f'Sorry, but there were {len(search_spell_results)} results! Please try to be more specific.'

    # Tell user if there was not a single result
    else:
        out = 'Sorry, but no such spell could be found!'

    # Send the spell search response
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


try:
    if sys.argv[1] == 'handle_signal':
        signal.signal(signal.SIGTERM, sigterm_handler)
except Exception as serr:
    logging.exception(serr)


# Run the bot
try:
    logging.info('Starting...')
    bot.start()

except Exception as err:
    logging.exception(err)

finally:
    logging.info('Exiting...')
