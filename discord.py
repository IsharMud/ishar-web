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

@slash_command(name="deadhead", description="Which player has died most?")
async def deadhead_function(ctx: SlashContext):
    """List which player has the highest number of total deaths."""
    leader = await Player.objects.order_by("-statistics__total_deaths").afirst()
    deaths = await PlayerStat.objects.aget(player_id=leader.id)
    await ctx.send(
        f"_{leader.player_name}_ has died {deaths.total_deaths} times. :skull_crossbones:"
    )


@slash_command(name="faq", description="Frequently Asked Questions")
async def faq_function(ctx: SlashContext):
    """Link the website FAQ page."""
    await ctx.send("https://isharmud.com/faq/#faq")


@slash_command(name="leader", description="Who is the leading player?")
async def leader_function(ctx: SlashContext):
    """Leader."""
    leader = await Leader.objects.afirst()
    await ctx.send(
        f"_{leader.player_name}_ is the leading player!"
        f" :trophy: <https://isharmud.com/leaders/#leaders>"
    )


@slash_command(
    name="start",
    description=f"Get started playing {settings.WEBSITE_TITLE}!"
)
async def start_function(ctx: SlashContext):
    """Link the website getting started guide."""
    await ctx.send("https://isharmud.com/start/#start :rocket:")


"""
Start.
"""

# Start the Discord bot.
bot.start(settings.DISCORD["TOKEN"])
