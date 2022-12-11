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
from sentry import sentry_sdk


# Logging configuration
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S %Z'
)

# Connect/authenticate Ishar MUD Discord bot
bot = interactions.Client(
    token=discord_secret.TOKEN,
    default_scope=discord_secret.GUILD
)


# Method to get the details of a single help topic
def get_single_help(topic=None):
    """Return extended output for a single help topic"""

    # Get the single topic name and link
    url = f"<https://isharmud.com/help/{topic['name']}>".replace(' ', '%20')
    out = f"{topic['name']}: {url}\n"

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


# /challenges
@bot.command()
async def challenges(ctx: interactions.CommandContext):
    """Show the current in-game Ishar MUD challenges"""
    logging.info('%s (%i) / %s / challenges',
                 ctx.channel, ctx.channel_id, ctx.user)
    completed = 0
    all_challenges = Challenge.query.filter_by(is_active=1).all()
    for challenge in all_challenges:
        if challenge.winner_desc != '':
            completed = completed + 1
    total = len(all_challenges)
    await ctx.send(f'Challenges: {completed} completed / {total} total!')
    db_session.close()


# /deadhead
@bot.command()
async def deadhead(ctx: interactions.CommandContext):
    """Show the player with the most in-game deaths"""
    logging.info('%s (%i) / %s / deadhead',
                 ctx.channel, ctx.channel_id, ctx.user)
    deadman = Player.query.filter_by(
        is_deleted=0, game_type=0).order_by(-Player.deaths).first()
    out = 'The player who has died most is: '
    out += f'{deadman.name} - {deadman.deaths} times! ☠️'
    await ctx.send(out)
    db_session.close()


# /mudhelp <search>
@bot.command(
    name='mudhelp',
    description='Find Ishar MUD help topic',
    options=[
        interactions.Option(
            name='search',
            description='title of a help topic to search for',
            type=interactions.OptionType.STRING,
            required=True
        )
    ]
)
async def mudhelp(ctx: interactions.CommandContext, search: str):
    """Search for MUD help topics"""
    logging.info('%s (%i) / %s / mudhelp: "%s"',
                 ctx.channel, ctx.channel_id, ctx.user, search)

    # Try to find any help topics containing the search term
    ephemeral = True
    search_topics = search_help_topics(all_topics=None, search=search)

    # By default, tell user if there were no results
    out = 'Sorry, but no such help topics could be found!'
    if search_topics:

        # Handle single search result, if there is only one
        num_results = len(search_topics)
        if num_results == 1:
            ephemeral = False
            found_topic = next(iter(search_topics.values()))
            out = get_single_help(topic=found_topic)

        # Link search results to user, if there are multiple results
        elif num_results > 1:
            url = f'<https://isharmud.com/help/{search}>'.replace(' ', '%20')
            out = f'Search Results: {url} ({num_results} topics)'

    # Send the help search response
    await ctx.send(out, ephemeral=ephemeral)
    db_session.close()


# /spell <search>
@bot.command(
    name='spell',
    description='Find Ishar MUD spell help',
    options=[
        interactions.Option(
            name='search',
            description='name of a spell to search for',
            type=interactions.OptionType.STRING,
            required=True
        )
    ]
)
async def spell(ctx: interactions.CommandContext, search: str):
    """Search for spells in MUD help topics"""
    logging.info('%s (%i) / %s / spell: "%s"',
                 ctx.channel, ctx.channel_id, ctx.user, search)

    # Try to find any help topics containing the search term
    ephemeral = True
    search_results = search_help_topics(
        all_topics=None,
        search=search
    )

    # Narrow down the results to any topic named starting with "Spell "
    search_spell_results = {}
    for name, topic in search_results.items():
        if name.startswith('Spell '):
            search_spell_results[name] = topic

    # By default, tell user if there were no results
    out = 'Sorry, but no such spell(s) could be found!'

    if search_spell_results:

        # Handle single search result, if there is only one
        num_results = len(search_spell_results)
        if num_results == 1:
            ephemeral = False
            found_spell = next(iter(search_spell_results.values()))
            out = get_single_help(topic=found_spell)

        # Show user the matching spell names, if there were 10 or less
        elif num_results <= 10:
            out = f'Found {num_results} spells: '
            out += ", ".join(search_spell_results.keys())

        # Otherwise, tell them to be more specific
        else:
            out = f'Sorry, but there were {num_results} results! '
            out += 'Please try to be more specific.'

    # Send the spell search response
    await ctx.send(out, ephemeral=ephemeral)
    db_session.close()


# /season
@bot.command()
async def season(ctx: interactions.CommandContext):
    """Show the current Ishar MUD season"""
    logging.info('%s (%i) / %s / season',
                 ctx.channel, ctx.channel_id, ctx.user)
    current = Season.query.filter_by(
        is_active=1).order_by(-Season.season_id).first()
    out = f'It is currently Season {current.season_id}'
    out += f', which ends in {current.expires}!'
    await ctx.send(out)
    db_session.close()


# /faq
@bot.command()
async def faq(ctx: interactions.CommandContext):
    """Link to the Frequently Asked Questions page"""
    logging.info('%s (%i) / %s / faq', ctx.channel, ctx.channel_id, ctx.user)
    await ctx.send('https://isharmud.com/faq')


# /faqs
@bot.command()
async def faqs(ctx: interactions.CommandContext):
    """Link to the Frequently Asked Questions page"""
    logging.info(
        '%s (%i) / %s / faqs',
        ctx.channel, ctx.channel_id, ctx.user
    )
    await ctx.send('https://isharmud.com/faq')


# /get_started
@bot.command()
async def get_started(ctx: interactions.CommandContext):
    """Link to the Getting Started page"""
    logging.info(
        '%s (%i) / %s / get_started',
        ctx.channel, ctx.channel_id, ctx.user
    )
    await ctx.send('https://isharmud.com/get_started')


# /getstarted
@bot.command()
async def getstarted(ctx: interactions.CommandContext):
    """Link to the Getting Started page"""
    logging.info('%s (%i) / %s / getstarted',
                 ctx.channel, ctx.channel_id, ctx.user)
    await ctx.send('https://isharmud.com/get_started')


# Handle SIGTERM
def sigterm_handler(num, frame):
    """Try to exit gracefully on SIGTERM"""
    logging.info('Caught SIGTERM: %i / %s', num, frame)
    sys.exit(0)


# Run the bot
try:
    logging.info('Starting...')
    signal.signal(signal.SIGTERM, sigterm_handler)
    bot.start()

# Catch exceptions/errors, and exit with an error code (1)
except Exception as err:
    logging.exception(err)
    sentry_sdk.capture_exception(err)
    sys.exit(1)

# Say goodbye
finally:
    logging.info('Exiting...')
