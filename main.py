from db.models import Anime, AnimeState, State, AnimeGenre, Genre
from db.actions import DataBase
from scraping.main import FactoryListAnime as fla


if __name__ == '__main__':
    DataBase.create_tables()
    DataBase.update_database()
