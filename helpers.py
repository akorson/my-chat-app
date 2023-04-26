import requests
from bs4 import BeautifulSoup

class SearchEngines:
    def __init__(self, bing_key):
        self.bing_key = bing_key

    def search(self, query, search_engine):
        if search_engine == 'Google':
            return self.search_google(query)
        elif search_engine == 'Scholar':
            return self.search_scholar(query)
        elif search_engine == 'DuckDuckGo':
            return self.search_duckduckgo(query)
        elif search_engine == 'Bing':
            return self.search_bing(query)
        else:
            return []

    def search_google(self, query):
        url = f'https://www.google.com/search?q={query}'
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'}
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.content, 'html.parser')
        results = []
        for result in soup.find_all('div', {'class': 'r'}):
            link = result.find('a')
            title = link.text.strip()
            href = link['href']
            results.append((title, href))
        return results

    def search_scholar(self, query):
        url = f'https://scholar.google.com/scholar?hl=en&as_sdt=0%2C5&q={query}&btnG='
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'}
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.content, 'html.parser')
        results = []
        for result in soup.find_all('div', {'class': 'gs_ri'}):
            link = result.find('a')
            title = link.text.strip()
            href = link['href']
            results.append((title, href))
        return results

    def search_duckduckgo(self, query):
        url = f'https://duckduckgo.com/html/?q={query}'
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'}
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.content, 'html.parser')
        results = []
        for result in soup.find_all('a', {'class': 'result__url'}):
            title = result.text.strip()
            href = result['href']
            results.append((title, href))
        return results

    def search_bing(self, query):
        headers = {
            'Ocp-Apim-Subscription-Key': self.bing_key
        }
        params = {
            'q': query,
            'count': 10,
            'mkt': 'en-US',
            'safeSearch': 'Moderate'
        }
        response = requests.get('https://api.cognitive.microsoft.com/bing/v7.0/search', headers=headers, params=params)
results = []
for result in response.json()['webPages']['value']:
    results.append((result['name'], result['url']))
return results
