import peewee as pw
from scraping.main import AnimeScraping
from .models import Genre, Anime, AnimeGenre, AnimeRelation, Episode


class DataBase:

    @staticmethod
    def create_tables():
        if not Genre.table_exists():
            Genre.create_table()
        if not Anime.table_exists():
            Anime.create_table()
        if not AnimeGenre.table_exists():
            AnimeGenre.create_table()
        if not AnimeRelation.table_exists():
            AnimeRelation.create_table()
        if not Episode.table_exists():
            Episode.create_table()

    @staticmethod
    def create_anime_record(anime):
        
        if not isinstance(anime, AnimeScraping):
            raise TypeError("anime must be a AnimeScraping")
        
        anime_record = Anime.create(**anime.to_db())
        anime_record.save()
        for i in anime.genres:
            genre, created = Genre.get_or_create(genre=i)
            animeGenre_record = AnimeGenre.create(anime=anime_record, genre=genre)
            animeGenre_record.save()
        for i in anime.animeRel_to_db():
            i['anime'] = anime_record
            animeRelation_record = AnimeRelation.create(**i)
            animeRelation_record.save()
        for i in anime.episode_list_to_db():
            i['anime'] = anime_record
            episode_record = Episode.create(**i)
            episode_record.save()
        
        
