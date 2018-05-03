import peewee as pw
from .settings import DATABASE


class BaseModel(pw.Model):
    """A base model that will use our Sqlite database."""
    class Meta:
        database = DATABASE

class Genre(BaseModel):
    genre = pw.CharField(unique=True)

    class Meta:
        db_table = 'Genres'

class State(BaseModel):
    state = pw.CharField(unique=True)

    class Meta:
        db_table = 'States'

class Anime(BaseModel):
    aid = pw.IntegerField(unique=True)
    slug = pw.CharField(unique=True)
    url = pw.CharField(unique=True)
    name = pw.CharField()
    anime_type = pw.CharField()
    image = pw.CharField()
    synopsis = pw.CharField(null=True)

    class Meta:
        db_table = 'Animes'

class AnimeGenre(BaseModel):
    anime = pw.ForeignKeyField(Anime)
    genre = pw.ForeignKeyField(Genre)

    class Meta:
        db_table = 'AnimesGenres'

class AnimeState(BaseModel):
    anime = pw.ForeignKeyField(Anime)
    state = pw.ForeignKeyField(State)

    class Meta:
        db_table = 'AnimesStates'

class AnimeRelation(BaseModel):
    url = pw.CharField()
    rel = pw.CharField()
    aid = pw.CharField()
    slug = pw.CharField()
    anime = pw.ForeignKeyField(Anime, related_name='anime_related')

    class Meta:
        db_table = 'AnimeRelations'

class Episode(BaseModel):
    name = pw.CharField()
    url = pw.CharField(unique=True)
    image = pw.CharField()
    anime = pw.ForeignKeyField(Anime, related_name='anime')

    class Meta:
        db_table = 'Episodes'
