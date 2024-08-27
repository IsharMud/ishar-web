def parse_stats(line: str) -> list:
    """Parse text right of colon, from "Stats  : " in single line."""
    stats_line = line.split(" : ")[1].strip()
    stats = []
    for splitter in (",", "|", "/"):
        stats_split = stats_line.split(splitter)
        for stat_item in stats_split:
            stat_item = stat_item.strip()
            stats.append(stat_item)
    return stats
