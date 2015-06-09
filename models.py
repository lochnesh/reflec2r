from peewee import *
import os

database = MySQLDatabase(os.getenv('REFL_DBNAME', '?'), 
                         **{'host': os.getenv('REFL_DBHOST', '?'), 
                            'password': os.getenv('REFL_DBPW', '?'), 
                            'user': os.getenv('REFL_DBUN', '?')})

class UnknownField(object):
    pass

class BaseModel(Model):
    class Meta:
        database = database

class Reflector(BaseModel):
    id = IntegerField(primary_key=True, db_column='id', null=False)
    amount = CharField(null=True)
    date = DateTimeField(null=True)
    refund = IntegerField(db_column='refund_id', null=True)
    tx = IntegerField(db_column='tx_id', null=True)

    class Meta:
        db_table = 'reflector'

class ReflectorSettings(BaseModel):
    key = CharField(null=True, unique=True, primary_key=True)
    value = CharField(null=True)

    class Meta:
        db_table = 'reflector_settings'

class ReflectorTrusted(BaseModel):
    note = CharField(null=True)
    user = CharField(db_column='user_id', null=True)

    class Meta:
        db_table = 'reflector_trusted'

