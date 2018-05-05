from db.models import Anime, AnimeState, State, AnimeGenre, Genre
from db.actions import DataBase
from scraping.main import FactoryListAnime as fla
import sys


if __name__ == '__main__':
    DataBase.create_tables()
    while True:
        print("""
    1: Actualizar toda la base de datos y salir.
    2: Actualizar animes en emision y salir.
    3: Salir.
    """
        )
        e = input("Seleccione una opción: ")
        if e == "1":
            DataBase.update_database()
            break
        elif e == "2":
            DataBase.update_animes_in_emision()
            break
        elif e == "3":
            break
        else:
            print("Entrada no valida.")
