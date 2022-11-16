# TODO

## Fun Features

### Fancy sortable and filter-able tables for leader board
-  Maybe this?
    * https://blog.miguelgrinberg.com/post/beautiful-interactive-tables-for-your-flask-templates

## New Pages

### Who list (/who)
- Should it check sockets or the database?
    * Why not both?

## Bugs

### SQLAlchemy deletes need to cascade properly
- _Currently_, players need to have their related records deleted first/separately before `Player`, like so:

    ```
    db_session.query(models.PlayersFlag).filter_by(player_id = del_id).delete()
    db_session.query(models.PlayerQuest).filter_by(player_id = del_id).delete()
    db_session.query(models.PlayerRemortUpgrade).filter_by(player_id = del_id).delete()
    db_session.query(models.Player).filter_by(id = del_id).delete()
    ```
