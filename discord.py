#!/usr/bin/env python3
import traceback

from django import setup
from django.conf import settings
from django.utils import timezone
from django.utils.timesince import timeuntil
from interactions import Client, Intents, listen, slash_command, SlashContext
from interactions.api.events import CommandError


"""
Set up.
"""
setup()

from apps.seasons.utils.current import aget_current_season


@listen()
async def on_ready():
    """Say so when the bot is ready!"""
    print(f"Ready! ({bot})")


@listen()
async def on_message_create(event):
    """Print message link."""
    print(f"{event.message.jump_url}")


@listen(CommandError, disable_default_listeners=True)
async def on_command_error(event: CommandError):
    """Print errors."""
    traceback.print_exception(event.error)
    if not event.ctx.responded:
        await event.ctx.send("Something went wrong.")


"""
Commands.
"""

@slash_command(name="challenges", description=f"{settings.WEBSITE_TITLE} Challenges")
async def challenges_function(ctx: SlashContext):
    """Link the website challenges page with count of complete/incomplete."""
    from apps.challenges.models import Challenge

    complete = await Challenge.objects.filter(is_active__exact=1).exclude(winner_desc__exact="").acount()
    incomplete = await Challenge.objects.filter(is_active__exact=1).filter(winner_desc__exact="").acount()
    url = "https://isharmud.com/challenges/#challenges"
    await ctx.send(
        f" [Challenges]({url}) {complete} complete -"
        f" {incomplete} incomplete :crossed_swords:"
    )


@slash_command(name="cycle", description=f"When do {settings.WEBSITE_TITLE} challenges cycle?")
async def cycle_function(ctx: SlashContext):
    """List when challenges next cycle."""
    current = await aget_current_season()
    next = current.get_next_cycle()
    timestamp = next.strftime("%A, %B %d, %I:%M:%S %p %Z")
    await ctx.send(
        "Challenges cycle in"
        f" **{timeuntil(next)}** at `{timestamp}` :arrows_counterclockwise:",
    )


@slash_command(name="deadhead", description=f"Which {settings.WEBSITE_TITLE} player has died most?")
async def deadhead_function(ctx: SlashContext):
    """List which player has the highest number of total deaths."""
    from apps.players.models import Player, PlayerStat

    leader = await Player.objects.order_by("-statistics__total_deaths").afirst()
    deaths = await PlayerStat.objects.aget(player_id=leader.id)
    await ctx.send(
        f"_{leader.name}_ has died {deaths.total_deaths} times. :skull_crossbones:"
    )


@slash_command(name="faq", description=f"{settings.WEBSITE_TITLE} Frequently Asked Questions")
async def faq_function(ctx: SlashContext):
    """Link the website FAQ page."""
    await ctx.send("https://isharmud.com/faq/#faq :question:")


@slash_command(name="leader", description=f"Who is the leading {settings.WEBSITE_TITLE} player?")
async def leader_function(ctx: SlashContext):
    """Leader."""
    from apps.leaders.models import Leader

    leader = await Leader.objects.afirst()
    await ctx.send(
        f"_{leader.name}_ is the leading player!"
        f" :trophy: <https://isharmud.com/leaders/#leaders>"
    )


@slash_command(name="mudtime", description=f"What is the {settings.WEBSITE_TITLE} time?")
async def mudtime_function(ctx: SlashContext):
    """Show the MUD time."""
    timestamp = timezone.now().strftime("%A, %B %d, %Y @ %I:%M:%S %p %Z")
    await ctx.send(
        f"The current {settings.WEBSITE_TITLE} time"
        f" is `{timestamp}` :clock:"
    )


@slash_command(name="season", description=f"What {settings.WEBSITE_TITLE} season is it?")
async def season_function(ctx: SlashContext):
    """Season."""
    current = await aget_current_season()
    expires = current.expiration_date
    url = "https://isharmud.com/season/#season"
    await ctx.send(
        f"[Season {current.season_id}]({url})"
        f" :hourglass_flowing_sand: ends in {timeuntil(expires)}"
        f" :alarm_clock: {expires.strftime('%A, %B %d, %Y')}"
    )


@slash_command(name="start", description=f"Get started playing {settings.WEBSITE_TITLE}!")
async def start_function(ctx: SlashContext):
    """Link the website getting started guide."""
    await ctx.send("https://isharmud.com/start/#start :rocket: :joystick:")


@slash_command(name="wiki", description=f"{settings.WEBSITE_TITLE} Wiki")
async def wiki_function(ctx: SlashContext):
    """Link the wiki."""
    await ctx.send(f"{settings.WIKI_URL} :globe_with_meridians: ")


"""
Start.
"""

bot_settings = {
    intents=Intents.DEFAULT
}
if settings.DEBUG:
    bot_settings["debug_scope"] = settings.DISCORD["GUILD"]

bot = Client(**bot_settings)

# Start the Discord bot.
bot.start(settings.DISCORD["TOKEN"])
