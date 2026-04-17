#!/usr/bin/env python3

from django import setup
from django.conf import settings
from interactions import Client, Intents, listen, slash_command, SlashContext


"""
Set up.
"""
setup()
bot = Client(intents=Intents.DEFAULT)

from apps.leaders.models import Leader
from apps.players.models import Player, PlayerStat


@listen()
async def on_ready():
    """Say so when the bot is ready!"""
    print(f"Ready! ({bot})")


#@listen()
#async def on_message_create(event):
#    print(f"Message: {event.message.jump_url}")


"""
Commands.
"""

@slash_command(name="challenges", description=f"{settings.WEBSITE_TITLE} Challenges")
async def challenges_function(ctx: SlashContext):
    """Link the website challenges page."""
    await ctx.send("https://isharmud.com/challenges/#challenges :crossed_swords:")


@slash_command(name="deadhead", description=f"Which {settings.WEBSITE_TITLE} player has died most?")
async def deadhead_function(ctx: SlashContext):
    """List which player has the highest number of total deaths."""
    leader = await Player.objects.order_by("-statistics__total_deaths").afirst()
    deaths = await PlayerStat.objects.aget(player_id=leader.id)
    await ctx.send(
        f"_{leader.name}_ has died {deaths.total_deaths} times. :skull_crossbones:"
    )


@slash_command(name="faq", description=f"{settings.WEBSITE_TITLE} Frequently Asked Questions")
async def faq_function(ctx: SlashContext):
    """Link the website FAQ page."""
    await ctx.send("https://isharmud.com/faq/#faq :question:")


@slash_command(
    name="leader",
    description=f"Who is the leading {settings.WEBSITE_TITLE} player?"
)
async def leader_function(ctx: SlashContext):
    """Leader."""
    leader = await Leader.objects.afirst()
    await ctx.send(
        f"_{leader.name}_ is the leading player!"
        f" :trophy: <https://isharmud.com/leaders/#leaders>"
    )


@slash_command(name="season", description=f"What {settings.WEBSITE_TITLE} season is it?")
async def season_function(ctx: SlashContext):
    """Link the website season page."""
    # TODO: Avoid django.core.exceptions.SynchronousOnlyOperation
    #   with Season utils.get_current_season.
    await ctx.send(f"https://isharmud.com/season/#season :sunrise_over_mountains:")


@slash_command(
    name="start",
    description=f"Get started playing {settings.WEBSITE_TITLE}!"
)
async def start_function(ctx: SlashContext):
    """Link the website getting started guide."""
    await ctx.send("https://isharmud.com/start/#start :rocket: :joystick:")


@slash_command(
    name="wiki",
    description=f"{settings.WEBSITE_TITLE} Wiki"
)
async def wiki_function(ctx: SlashContext):
    """Link the wiki."""
    await ctx.send(f"{settings.WIKI_URL} :globe_with_meridians: ")


"""
Start.
"""

# Start the Discord bot.
bot.start(settings.DISCORD["TOKEN"])
