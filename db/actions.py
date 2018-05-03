import peewee as pw
from scraping.main import AnimeScraping
from scraping.main import FactoryListAnime as fla
from db.settings import DATABASE 
from .models import Genre, Anime, AnimeGenre, AnimeRelation, Episode, State, AnimeState


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
        if not State.table_exists():
            State.create_table()
        if not AnimeState.table_exists():
            AnimeState.create_table()

    @staticmethod
    def create_anime_record(anime):
        
        if not isinstance(anime, AnimeScraping):
            raise TypeError("anime must be a AnimeScraping")
        
        anime_record = Anime.create(**anime.to_db())
        anime_record.save()
        for i in anime.genres:
            genre, created = Genre.get_or_create(genre=i)
            AnimeGenre.create(anime=anime_record, genre=genre).save()
        state, created = State.get_or_create(state=anime.state)
        AnimeState.create(anime=anime_record, state=state).save()

        for i in anime.animeRel_to_db():
            i['anime'] = anime_record
            AnimeRelation.create(**i).save()
        for i in anime.episode_list_to_db():
            i['anime'] = anime_record
            Episode.create(**i).save()
    
    @staticmethod
    def update_anime(anime):
    
        if not isinstance(anime, Anime):
            raise TypeError("anime must be a Anime")

        anime_data = fla.get_anime(anime.url)

        if anime.aid != anime_data.aid:
            anime.aid = anime_data.aid
        if anime.slug != anime_data.slug:
            anime.slug = anime_data.slug
        if anime.url != anime_data.url:
            anime.url = anime_data.url
        if anime.name != anime_data.name:
            anime.name = anime_data.name
        if anime.anime_type != anime_data.anime_type:
            anime.anime_type = anime_data.anime_type
        if anime.image != anime_data.image:
            anime.image = anime_data.image
        if anime.synopsis != anime_data.synopsis:
            anime.synopsis = anime_data.synopsis

        anime.save()

        def update_genres(anime, anime_data):
            AnimeGenre.delete().where(AnimeGenre.anime == anime).execute()
            for i in anime_data.genres:
                genre, created = Genre.get_or_create(genre=i)
                AnimeGenre.create(anime=anime, genre=genre).save()
        query = (AnimeGenre
            .select()
            .where(AnimeGenre.anime == anime)
        )
        if len(query) != len(anime_data.genres):
            update_genres(anime, anime_data)
        else:
            for i in range(len(query)):
                if query[i].genre.genre != anime_data.genres[i]:
                    update_genres(anime, anime_data)
                    break


        def update_state(anime, anime_data):
            AnimeState.delete().where(AnimeState.anime == anime).execute()
            state, created = State.get_or_create(state=anime_data.state)
            AnimeState.create(anime=anime, state=state).save()
        
        query = AnimeState.get(AnimeState.anime == anime)
        if query.state.state != anime_data.state:
            update_state(anime, anime_data)


        def update_relations(anime, anime_data):
            AnimeRelation.delete().where(AnimeRelation.anime == anime).execute()
            for i in anime_data.animeRel_to_db():
                i['anime'] = anime
                AnimeRelation.create(**i).save()

        query = (AnimeRelation
            .select()
            .where(AnimeRelation.anime == anime)
        )
        if len(query) != len(anime_data.listAnmRel):
            update_relations(anime, anime_data)
        else:
            for i in range(len(query)):
                if (
                    query[i].aid != anime_data.listAnmRel[i].aid or 
                    query[i].rel != anime_data.listAnmRel[i].rel or
                    query[i].url != anime_data.listAnmRel[i].url
                    ):
                    update_relations(anime, anime_data)
                    break


        def update_episodes(anime, anime_data):
            Episode.delete().where(Episode.anime == anime).execute()
            for i in anime_data.episode_list_to_db():
                i['anime'] = anime
                Episode.create(**i).save()

        query = (Episode
            .select()
            .where(Episode.anime == anime)
        )
        if len(query) != len(anime_data.episode_list):
            update_episodes(anime, anime_data)
        else:
            for i in range(len(query)):
                if (
                    query[i].name != anime_data.episode_list[i].name or 
                    query[i].url != anime_data.episode_list[i].url or
                    query[i].image != anime_data.episode_list[i].image
                    ):
                    update_episodes(anime, anime_data)
                    break
        
    @staticmethod
    def update_animes_in_emision():
        query = (Anime
            .select()
            .join(AnimeState)
            .join(State)
            .where(State.state == 'En emision')
        )
        with DATABASE.atomic():
            for i in query:
                DataBase.update_anime(i)

    @staticmethod
    def update_database():
        links = fla.get_all_animes()
        with open('animes.txt', 'w') as text_file:
            with DATABASE.atomic():
                for i in links:
                    anime = fla.get_anime(i)
                    text_file.write(i+"\n")
                    try:
                        anime = Anime.get(aid=anime.aid)
                        DataBase.update_anime(anime)
                    except:
                        DataBase.create_anime_record(anime)
