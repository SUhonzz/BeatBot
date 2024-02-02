from datetime import datetime, date
from tinydb.storages import JSONStorage
from tinydb_serialization import Serializer, SerializationMiddleware
from tinydb_serialization.serializers import DateTimeSerializer


class DateSerializer(Serializer):
    # The class this serializer handles --> must be date instead of datetime.date
    OBJ_CLASS = date

    def encode(self, obj):
        return obj.isoformat()

    def decode(self, s):
        return datetime.fromisoformat(s).date()


serializer = SerializationMiddleware(JSONStorage)
serializer.register_serializer(DateTimeSerializer(), 'TinyDateTime')
serializer.register_serializer(DateSerializer(), 'TinyDate')