from peewee import Model, SqliteDatabase

database = SqliteDatabase('/home/ubuntu/SignalRecognition.db',
                          pragmas={'journal_mode': 'wal', ' cache_size': -1024 * 64})


class BaseModel(Model):
    class Meta:
        database = database
