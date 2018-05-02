from db.models import Anime, AnimeGenre, Genre
from db.actions import DataBase
from scraping.main import FactoryListAnime as fla

def create_all_animes_records():
    links = fla.get_all_animes()
    with open('animes.txt', 'w') as text_file:
        for i in links:
            anime = fla.get_anime(i)
            try:
                Anime.get(aid=anime.aid)
            except:
                DataBase.create_anime_record(anime)
            text_file.write(i+"\n")

if __name__ == '__main__':
    DataBase.create_tables()
    # fla.get_all_animes()
    create_all_animes_records()

    # query = (Anime
    #         .select()
    #         .join(AnimeGenre)
    #         .join(Genre)
    #         .where(Genre.genre == 'a')
    #      )
