from apps.processes.utils.process import get_process


def runtime():
    """Show the current server process runtime."""
    process = get_process()
    return "Running since %s (%s) :clock:" % (
        process.created.strftime("%A, %B %d, %Y @ %I:%M:%S %p %Z"),
        process.runtime()
    )
