import scrapy
import urlparse
import re
from websosanh.items import AdayroiItem

class AdayroiSpider(scrapy.Spider):
    name = "adayroi_spider"
    allowed_domains = ["adayroi.com"]
    start_urls = [
        "https://www.adayroi.com/dien-thoai-di-dong-m323",
        "https://www.adayroi.com/may-tinh-bang-m328",
        "https://www.adayroi.com/may-tinh-xach-tay-m350",
        "https://www.adayroi.com/may-tinh-de-ban-m353"
    ]    

    # def parse(self, response): 
    #     nav_wrapper = response.xpath('.//*[@class="c-second-menu__item c-second-menu__item_style_heading2"]/a/@href')

    #     links = []
    #     for i in nav_wrapper:
    #         if str(i.extract()) not in links: 
    #             links.append(str(i.extract()))

    #     links.pop() 
    #     for url in links:
    #         yield scrapy.Request(url, callback=self.parse_all_pagination)


    def parse(self, response):
        item = AdayroiItem()
        category_dict = {
            "https://www.adayroi.com/dien-thoai-di-dong-m323": 'cellphone',
            "https://www.adayroi.com/may-tinh-bang-m328": 'tablet',
            "https://www.adayroi.com/may-tinh-xach-tay-m350": 'laptop',
            "https://www.adayroi.com/may-tinh-de-ban-m353": 'desktop'
        }

        first_url = response.xpath('.//div[contains(@class,"pagination")]/a[@data-paging="first"]/@href').extract_first()
        last_url = response.xpath('.//div[contains(@class,"pagination")]/a[@data-paging="last"]/@href').extract_first()
        first = int(urlparse.parse_qs(urlparse.urlparse(first_url).query)['p'][0])
        last = int(urlparse.parse_qs(urlparse.urlparse(last_url).query)['p'][0])

        category_url = response.urljoin("")
        item['category'] = category_dict[category_url]

        pagination_links = [response.urljoin("?p=")+`page` for page in range(first, last + 1)]

        for url in pagination_links:
            yield scrapy.Request(url, callback=self.parse_each_pagination, meta={'item': item})

    def parse_each_pagination(self, response):
        item = response.meta['item']
        base_url = "http://www.adayroi.com"                     
        for href in response.xpath('.//span[@class="mask"]/a/@href'):
            url = base_url + href.extract()
            yield scrapy.Request(url, callback=self.parse_product, meta={'item': item})          

    def parse_product(self, response):
        item = response.meta['item']
        item['url'] = response.urljoin("")

        item['title'] = response.xpath('.//h1[@class="item-title"]/text()').extract_first()
        # image_url
        item['image_url'] = response.xpath('.//div[@class="stage"]/img/@src').extract_first()

        # price
        sale_price = response.xpath('.//div[@class="item-price"]/text()').extract_first()
        item['sale_price'] = re.sub('[^0-9.]', '', sale_price)
        regular_price = response.xpath('.//span[contains(@class,"value") and contains(@class,"original")]/text()').extract_first()
        item['regular_price'] = re.sub('[^0-9.]', '', regular_price)
        item['product_saving'] = response.xpath('.//span[contains(@class,"rate") and contains(@class,"discount")]/text()').extract_first()
        yield item