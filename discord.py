#!/usr/bin/env python3

from django.conf import settings
from interactions import Client, Intents, listen, slash_command, SlashContext

from apps.leaders.models import Leader


"""
Set up.
"""
bot = Client(intents=Intents.DEFAULT)

@listen()
async def on_ready():
    """Say so when the bot is ready!"""
    print("Ready!")
    print(f"bot:{bot}")


#@listen()
#async def on_message_create(event):
#    print(f"Message: {event.message.jump_url}")


"""
Commands.
"""

@slash_command(name="deadhead", description="Which player has died most?")
async def deadhead_function(ctx: SlashContext):
    """List which player has the highest number of deaths."""
    await ctx.send("The player who has died most is __TODO__. Sorry.")


@slash_command(name="faq", description="Frequently Asked Questions")
async def faq_function(ctx: SlashContext):
    """Link the website FAQ page."""
    await ctx.send("https://isharmud.com/faq/#faq")


@slash_command(name="leader", description="Who is the leading player?")
async def leader_function(ctx: SlashContext):
    """Leader."""
    leader = Leader.objects.first()
    await ctx.send(
        f"_{leader.player_title}_ is the leading player!"
        f" <https://isharmud.com/leaders/#leaders>"
    )


@slash_command(
    name="start",
    description=f"Get started playing {settings.WEBSITE_TITLE}!"
)
async def start_function(ctx: SlashContext):
    """Link the website getting started guide."""
    await ctx.send("https://isharmud.com/start/#start")


"""
Start.
"""

# Start the Discord bot.
bot.start(settings.DISCORD["TOKEN"])
