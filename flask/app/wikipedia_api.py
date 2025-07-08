from sqlalchemy.orm import backref
import wikipediaapi
import wikipedia


class WikipediaApi:
    def __init__(self):
        self.wiki = wiki = wikipediaapi.Wikipedia("en")

    def get_wiki_genre_url(self, genre_name: str):
        """gets the URL to the Wikipedia page of the given genre

        Args:
            genre_name (str): the name of the genre you want the page of
        """
        wiki_page = self.get_wiki_genre_page(genre_name)
        genre_url = None
        if wiki_page:
            # genre_url = wiki_page.fullurl
            genre_url = wiki_page.canonicalurl
        return genre_url

    def get_wiki_genre_page(self, genre_name: str) -> wikipediaapi.WikipediaPage:
        search_results = wikipedia.search(genre_name, results=15)
        all_genre_page = self.wiki.page("List of music styles")
        genre_page = None
        for result in search_results:
            page = self.wiki.page(result)
            if result in self.wiki.links(all_genre_page):
                genre_page = self.wiki.page(result)
                break
        return genre_page

    def get_wiki_genre_urls_dict(self, genre_names):
        urls_dict = {}
        for genre_name in genre_names:
            urls_dict[genre_name] = self.get_wiki_genre_url(genre_name)
        return urls_dict

    def get_wiki_genre_list(self):
        # https://en.wikipedia.org/wiki/List_of_music_styles
        all_genre_page = self.wiki.page("List of music styles")
        all_genre_links = list(self.wiki.links(all_genre_page).keys())
        link_filter = [
            "List of",
            ":",
            "s in music",
            "-century",
            "Music_genre",
            "Styles of" "AllMusic",
            "Genealogy_of_musical_genres",
            "Simon_Frith",
        ]
        all_genre_list = [
            link
            for link in all_genre_links
            if not any(filtered_symbol in link for filtered_symbol in link_filter)
        ]
        return all_genre_list

    def update_genres(self):
        self.genres = []
        wiki_genre_list = self.get_wiki_genre_list()
        first_three = wiki_genre_list[:3]
        for genre_name in wiki_genre_list:
            page = self.wiki.page(genre_name)
            description = page.summary
            super_genres = None
            sub_genres = None
            try:
                wiki_url = page.canonicalurl
            except:
                wiki_url = None

            genre = GenreNotInDb(
                name=genre_name,
                description=description,
                super_genres=super_genres,
                sub_genres=sub_genres,
                wiki_url=wiki_url,
            )
            self.genres.append(genre)


class GenreNotInDb:
    def __init__(self, name, description, super_genres, sub_genres, wiki_url):
        self.name = name
        self.description = description
        self.super_genres = super_genres
        self.sub_genres = sub_genres
        self.wiki_url = wiki_url

    def __repr__(self):
        return "Genre named \"{self.name}\" with url '{self.wiki_url}'. The SuperGenres are {self.super_genres} and the SubGenres are {self.sub_genres}.\nDescription: {self.description}".format(
            self=self
        )


if __name__ == "__main__":
    wikipedia_api = WikipediaApi()
    # url = wikipedia_api.get_wiki_genre_url('uk dnb')
    # print(url)
    # print(wikipedia_api.get_wiki_genre_list())
    # print(len(wikipedia_api.get_wiki_genre_list()))
    wikipedia_api.update_genres()
    with open(file="genres.txt", mode="w", encoding="utf-8") as file:
        for genre in wikipedia_api.genres:
            file.write(str(genre) + "\n")
