def parse_stats(line: str) -> list:
    """Parse text right of colon, from "Stats  : " in single line."""
    stats_line = line.split(" : ")[1].strip()
    stats = []
    for splitter in (",", "|", "/"):
        if splitter in stats_line:
            for stat_item in stats_line.split(splitter):
                stat_item = stat_item.strip()
                stats.append(stat_item)
    if not stats:
        stats.append(stats_line)
    return stats
