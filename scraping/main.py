import requests
from bs4 import BeautifulSoup
from bs4.element import Tag


class FactoryListAnime:
    
    url = 'animeflv.net'

    @staticmethod
    def start_page_scraping(page=1):
        list_anime_links = []
        rute = '/browse?order=title&page={}'.format(page)
        response = requests.get("https://" + FactoryListAnime.url + rute)
        soup = BeautifulSoup(response.content, 'html.parser')
        listAnimes = soup.find_all('article', {'class':'Anime'})

        for i in listAnimes:
            link = i.find('a')['href']
            list_anime_links.append(link)

        return list_anime_links
    
    @staticmethod
    def get_total_pages():
        rute = '/browse'
        response = requests.get("https://" + FactoryListAnime.url + rute)
        soup = BeautifulSoup(response.content, 'html.parser')
        pagination = soup.find('ul', {'class': 'pagination'}).find_all('a')
        last_page = pagination[len(pagination)-2]['href'].split('page=')[-1]
        print("La cantidad total de paginas es: ", last_page)
        return int(last_page)
    
    @staticmethod
    def get_all_animes():
        a = FactoryListAnime.get_total_pages()
        list_anime_links = []
        for i in range(1, a+1):
            print("Analizando pagina: {}".format(i))
            tmpl = FactoryListAnime.start_page_scraping(i)
            list_anime_links += tmpl
        return list_anime_links
    
    @staticmethod
    def get_anime(url):
        print('Analizando: ', url)
        rute = url
        response = requests.get("https://" + FactoryListAnime.url + rute)
        soup = BeautifulSoup(response.content, 'html.parser')
        containers = soup.find_all('div', {'class': 'Container'})

        split = url.split('/')
        aid = int(split[2])
        slug = split[3]
        del split
        name = containers[1].find('h2', {'class': 'Title'}).string
        anime_type = containers[1].find('span', {'class': 'Type'}).string
        image = containers[2].find('div', {'class': 'AnimeCover'}).find('img')['src']
        state = containers[2].find('p', {'class': 'AnmStts'}).find('span').string
        synopsis = containers[2].find('div', {'class': 'Description'}).find('p').string
        genres = containers[2].find('nav', {'class': 'Nvgnrs'}).find_all('a')
        genres = [i.string for i in genres]
        episodes = containers[2].find('ul', {'class': 'ListCaps'}) or containers[2].find('ul', {'class': 'ListEpisodes'})
        has_next_ep = episodes.find('li', {'class': 'Next'})
        episodes = episodes.find_all('li')
        a, b = 1 if has_next_ep else 0, len(episodes)
        episode_list = []
        for i in range(a, b):
            ep_name_obj = episodes[i].find('p') or episodes[i].find('a')
            ep_name = ep_name_obj.string or ep_name_obj.get_text()
            ep_url = episodes[i].find('a')['href']
            ep_img = episodes[i].find('img', {'class': 'lazy'})
            if ep_img is not None:
                ep_img_url = ep_img['data-original']
            else:
                ep_img_url = ''
            episode_list.append(EpisodeScraping(ep_name, ep_url, ep_img_url))
        del a, b, has_next_ep, episodes
        listAnmRel = containers[2].find('ul', {'class': 'ListAnmRel'})
        if listAnmRel:
            cont_listAnmRel = listAnmRel.find_all('li')
            listAnmRel = []
            for i in cont_listAnmRel:
                link = i.find('a')['href']
                rel = str(i).split('</a>')[-1].split('</li>')[0]
                listAnmRel.append(AnimeReltionScraping(link, rel))
            del cont_listAnmRel
        else:
            listAnmRel = []

        return AnimeScraping(aid, url, slug, name, image, anime_type, state, synopsis, genres, episode_list, listAnmRel)


class EpisodeScraping:
    def __init__(self, name, url, image, *las, **kwargs):
        self.name = name
        self.url = url
        self.image = image
    
    def __str__(self):
        return str(self.name)
    
class AnimeReltionScraping:
    def __init__(self, url, rel, *args, **kwargs):
        self.url = url
        self.rel = rel
        self.aid = url.split('/')[2]
        self.slug = url.split('/')[3]

    def __str__(self):
        return self.aid + ":" + self.rel

class AnimeScraping:
    def __init__(self, aid, url, slug, name, image, anime_type, state, synopsis, genres, episode_list, listAnmRel, *args, **kwargs):
        self.aid = aid
        self.url = url
        self.slug = slug
        self.name = name
        self.image = image
        self.anime_type = anime_type
        self.state = state
        self.synopsis = synopsis
        self.genres = genres
        self.episode_list = episode_list
        self.listAnmRel = listAnmRel
    
    def __str__(self):
        string = """
aid: {}
url: {}
slug: {}
name: {}
self.image = {}
anime_type: {}
state: {}
synopsis: {}
genres: {}
episode_list: {}
listAnmRel: {}
        """.format(
                self.aid,
                self.slug,
                self.name,
                self.image,
                self.anime_type,
                self.state,
                self.synopsis,
                self.genres,
                str([str(i.name) for i in self.episode_list]),
                str([str(i) for i in self.listAnmRel])
            )
        return string

        
    def to_db(self):
        query = {
            'aid': self.aid,
            'url': self.url,
            'slug': self.slug,
            'name': self.name,
            'image': self.image,
            'anime_type': self.anime_type,
            'state': self.state,
            'synopsis': self.synopsis,
        }
        return query
    
    def animeRel_to_db(self):
        query_list = []
        for i in self.listAnmRel:
            query = {
                'url': i.url,
                'rel': i.rel,
                'aid': i.aid,
                'slug': i.slug
            }
            query_list.append(query)
        return query_list
    
    def episode_list_to_db(self):
        query_list = []
        for i in self.episode_list:
            query = {
                'name': i.name,
                'url': i.url,
                'image': i.image,
            }
            query_list.append(query)
        return query_list
