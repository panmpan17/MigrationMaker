# SQLAlchemy Migration Maker
SQLalchemy is a great DB manage python library. <br>
But it didn't have the built in migrate functionality. <br>

Inspire by django db manager, I write this package to migrate db more easily. <br>

Now, with this package can check db's model's version, and migrate to db with ease. <br>
Also can write your own migrate tool.

## Intall
`pip install sqlalchemy-migration-maker`

## Requiremnt
- sqlalchemy

## Testing
#### Require psycopg2
In my testing, I use postgres database to execute sql language

### Tested Envirment
- MacOSX
- Python3

### Tested Database
- Postgres