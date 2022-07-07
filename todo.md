# TODO

- Fix `PlayersFlags` model so `player.flags[45]` can be referenced more like `player.flags['PERM_DEATH']`
- Fancy sortable and filter-able tables for leader board
    * Maybe this? https://blog.miguelgrinberg.com/post/beautiful-interactive-tables-for-your-flask-templates
- Clean up format of birth, last log in & out, and time played on player pages
- Fix `create_isp`, `last_isp`, `create_ident`, and `last_ident` for new users and logins
- Fix `Quests` header on player pages to not depend on `players`.`quests_completed` to avoid empty space - like [Zot](https://isharmud.com/player/Zot)
