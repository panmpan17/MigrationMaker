# SQLAlchemy Migration Maker
[SQLalchemy](https://github.com/zzzeek/sqlalchemy) 是個 Python 的 Database Library，可以與 Postgres、MySQL 與其他 Database 連結，但是卻缺少了更新 Database 的功能。 <br>
受到 [Django](https://github.com/django/django) Database 的啟發，我寫了這套件使更新更輕鬆，把 Database 結構化成特別的 Id，並存到資料庫，透過比較結構來決定需要下哪些 SQL 指令。<br>
**此套件需要自行設定**

[SQLalchemy](https://github.com/zzzeek/sqlalchemy) is a  python library that deal with database. Can be used to connect with Postgres, MySQL, etc. But it lack of builtin migrate functionality. <br>
Inspire by django db manager, I write this package to migrate db more easily. <br>
It turn Database structure into special id then store in database. <br>
When there's new version structure, it compares two version then decide what SQL command need to be executed. <br>
**This package need to setup yourself**

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

## Example
model.py

```python
from sqlalchemy import Column
from sqlalchemy.types import Integer
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, autoincrement=True)

    def __repr__(self):
        return f"<User {self.id} {self.create_at}>"
 
```

migrate.py

```python
from .model import Base
from migrationmaker import VersionControl

version_ctl = VersionCtrol("{DB_URI}")

# 檢查版本控制是否存在於 DB
# Check version ctrl exist in DB
version_ctl.check_version_ctl_exist()

# 取回舊版本
# Retrieve old version
self.version_ctl.get_latest_version(is_old_metadata=True)

# 指定新版本
# Assign new version
self.version_ctl.new_version(Base.metadata)

if not self.version_ctl.check_same():
    self.version_ctl.migrate()

```