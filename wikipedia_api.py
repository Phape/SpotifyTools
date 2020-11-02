import wikipediaapi
import wikipedia


class WikipediaApi:
    def __init__(self):
        self.wiki = wiki = wikipediaapi.Wikipedia('en')

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
        all_genre_page = self.wiki.page('List of music styles')
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


if __name__ == "__main__":
    wikipedia_api = WikipediaApi()
    url = wikipedia_api.get_wiki_genre_url('uk dnb')
    print(url)
