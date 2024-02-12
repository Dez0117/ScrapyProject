import scrapy


class WikiFilmsSpider(scrapy.Spider):
    name = "wiki_films"
    allowed_domains = ["ru.wikipedia.org"]

    def start_requests(self):
        URL = "https://ru.wikipedia.org/w/index.php?title=%D0%9A%D0%B0%D1%82%D0%B5%D0%B3%D0%BE%D1%80%D0%B8%D1%8F%3A%D0%A4%D0%B8%D0%BB%D1%8C%D0%BC%D1%8B_%D0%BF%D0%BE_%D0%B0%D0%BB%D1%84%D0%B0%D0%B2%D0%B8%D1%82%D1%83&from=%D0%90"
        yield scrapy.Request(url=URL, callback=self.page_parse)

    def parse_film(self, response):

        film_info = {
            'title': response.xpath('//th[@colspan="2" and @scope="colgroup" and contains(@class, "infobox-above")]/text()').extract_first(),
            'genre': response.xpath('//tr/th[contains(., "Жанр") or contains(., "Жанры")]/following-sibling::td/span/a/text() | //tr/th[contains(., "Жанр") or contains(., "Жанры")]/following-sibling::td//a/text()').extract_first(),
            'stage_director': response.xpath('//th[contains(., "Режиссёр") or contains(., "Режиссёры")]/following-sibling::td/descendant::span/descendant::text()').extract_first(),
            'country': response.xpath('//tr/th[contains(., "Страна") or contains(., "Страны")]/following-sibling::td//a/span/text() | //tr/th[contains(., "Страна") or contains(., "Страны")]/following-sibling::td//a/text()').extract_first(),  # approved
            'year': response.xpath('//th[contains(., "Год")]/following-sibling::td//a/text() | //th[contains(., "Год")]/following-sibling::td//a/span/text()').extract_first()  # approved
        }
        yield film_info

    def page_parse(self, response):

        for url in response.xpath("//*[@class='mw-category-group']//a/@href").getall():
            yield response.follow(url, callback=self.parse_film)

        next_page = response.xpath('//*[@id="mw-pages"]/a[2]/@href').get()
        if next_page:
            yield response.follow(next_page, callback=self.page_parse)
