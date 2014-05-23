import json
import datetime

from schematics.models import Model
from schematics.types import StringType, URLType, ListType, ModelType, DateTimeType, DecimalType, BooleanType
from schematics.validate import validate
from schematics.transforms import blacklist
from schematics.types.serializable import serializable
from schematics.exceptions import ValidationError


class Song(Model):

    name = StringType(required=True)
    artist = StringType()
    url = URLType()


class Collection(Model):
    songs = ListType(ModelType(Song))


class WeatherReport(Model):
    city = StringType()
    temperature = DecimalType()
    taken_at = DateTimeType(default=datetime.datetime.now)

    @serializable
    def id(self):
        return('{0}:{1}'.format(self.city, self.temperature))

    class Options:
        serialize_when_none = False
        roles = {
            'public': blacklist('taken_at')
        }


class Signup(Model):
    name = StringType()
    call_me = BooleanType(default=False)

    def validate_call_me(self, data, value):
        if data['name'] == 'Brad' and data['call_me'] is True:
            raise ValidationError('He prefers email.')
        return value


def importing():

    song_json = '{"url": "http://www.youtube.com/watch?v=67KGSJVkix0", "name": "Werewolf", "artist": "Fiona Apple"}'
    fiona_song = Song(json.loads(song_json))
    print(fiona_song.url)


def Compound_Types():
    songs_json = '{"songs": [{"url": "https://www.youtube.com/watch?v=UeBFEanVsp4", "name": "When I Lost My Bet", "artist": "Dillinger Escape Plan"}, {"url": "http://www.youtube.com/watch?v=67KGSJVkix0", "name": "Werewolf", "artist": "Fiona Apple"}]}'
    song_collection = Collection(json.loads(songs_json))
    print(song_collection.songs[0])
    print(song_collection.songs[0].url)
    print(json.dumps(song_collection.to_primitive(), sort_keys=True, indent=4))


def validate_test():
    song1 = Song()
    song1.artist = 'Fiona Apple'
    song1.url = 'http://www.youtube.com/watch?v=67KGSJVkix0'
    # song1.validate()
    validate(Song, song1)


def coercion():
    dt_t = DateTimeType()
    dt = dt_t.to_native('2013-08-31T02:21:21.486072')
    print(dt, '\n', dt_t.to_primitive(dt))


def validate_string():
    st = StringType(max_length=10)
    print(st.to_native('this is longer than 10'))
    st.validate('this is longer than 10')


def simple_model():
    print(WeatherReport().to_native())
    wr = WeatherReport({'city': 'NYC', 'temperature': 80})
    print(wr.to_native(), wr.temperature, wr.taken_at)
    print(wr.to_primitive(role='public'))
    print(wr.id)


def model_validatior():
    try:
        su = Signup()
        su.name = 'Brad'
        su.validate()
        su.call_me = True
        print("Error's Here")
        su.validate()
    except ValidationError as ve:
        print(ve.messages)


importing()
Compound_Types()
# validate_test()
coercion()
# validate_string()
simple_model()
model_validatior()
