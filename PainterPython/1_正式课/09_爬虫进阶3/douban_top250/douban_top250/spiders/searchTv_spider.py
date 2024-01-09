from scrapy.spiders import Spider
from douban_top250.items import DoubanKeywordSearchResultItem
from scrapy import Request
from bs4 import BeautifulSoup
from urllib.parse import quote

class DoubanKeywordSearchSpider(Spider):
    name = "search_spider"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36',
    }

    def start_requests(self):
        
        search_text = quote("理想照耀中国")
        url = f'https://search.douban.com/movie/subject_search?search_text={search_text}'
        yield Request(url, headers=self.headers)
    def parse(self, response):
        if response.status != 200:
            print('请求失败')
            return
        # print(response.text)
        soup = BeautifulSoup(response.text,"html.parser",from_encoding="utf-8")
        soup = soup.find('div', {'class': 'grid-16-8 clearfix'})
        links = soup.find_all('a', {'class': ''})
        dmi = DoubanKeywordSearchResultItem()
        for item in links:
            link = item.get('href')
            print(link)
            dmi["link"] = link