"""Discord slash command handlers.

Importing this package triggers auto-registration of every command class
via the ``SlashCommand.__init_subclass__`` hook defined in ``base.py``.

To add a new command, create a module in this package with a class that
inherits from ``SlashCommand`` and set a ``name`` class attribute.
"""

# Import every command module so that subclass auto-registration fires.
from . import (  # noqa: F401
    challenges,
    cycle,
    deadhead,
    events,
    faq,
    feedback,
    leader,
    leaders,
    mudhelp,
    mudtime,
    runtime,
    season,
    upgrades,
    who,
)
