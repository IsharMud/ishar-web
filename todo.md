# TODO

## [Helptab](https://github.com/IsharMud/ishar-web/issues/19)

Reading the help (`helptab`) file is very complicated and messy...

Two possible solutions to simplify things would be to:
1) Migrate the `helptab` file to the database.
2) Implement a custom Django Manager to read the existing `helptab` file.

### Database
- Should each help topic be a row in a single "`help_topics`" database table?
  - Create a `help_topics` table...
  - Each row would be a single unique help topic.
    - Columns would be similar to:
      - `help_topic_id`
        - `int(10) primary key autoincrement not null`
      - `name`
        - `varchar(64) unique key not null`
      - `body`
        - `text not null`
      - `aliases`
        - `varchar(64)` (_comma-separate_?)
      - `syntax`
      - `minimum`
      - `saves`
      - `class`
      - `level`
        - `varchar(64)` ?


  - Help topics could probably be edited from Django administrative interface.
    
### Manager

- Custom Django [Manager](https://docs.djangoproject.com/en/4.2/topics/db/managers/) to read the help topics from the `helptab` file?
  - Each object would represent a single unique help topic.
    - `Commands`
    - `Spell Wizardlock`
    - `Inventory`
    - _etc._
  - Subsequently, each `help_topic` object would have (mostly string) attributes/properties similar to:
    - `name`
    - `body`
    - `aliases`
      - `list`/`tuple` of strings
    - `syntax`
    - `minimum`
    - `saves`
    - `class`
    - `level`
