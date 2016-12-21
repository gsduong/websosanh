import scrapy
import re
from websosanh.items import CellphonesItem

class CellphonesSpider(scrapy.Spider):
    name = "cellphones_spider"
    allowed_domains = ["cellphones.com.vn"]
    start_urls = [
        "https://cellphones.com.vn/mobile.html"
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
        item = CellphonesItem()
        category_dict = {
            "https://cellphones.com.vn/mobile.html": 'cellphone'
        }

        category_url = response.urljoin("")
        item['category'] = category_dict[category_url]
        nav_pagination = response.xpath('.//div[@class="pages"]//li/a/@href')
        if not nav_pagination:
            url = response.urljoin("")
            yield scrapy.Request(url, callback=self.parse_each_pagination, meta={'item': item})
        else:
            pagination_links = []
            pagination_links.append(response.urljoin(""));
            for page in nav_pagination: 
                if page.extract() not in pagination_links:
                    pagination_links.append(page.extract())
            for url in pagination_links:
                yield scrapy.Request(url, callback=self.parse_each_pagination, meta={'item': item})

    def parse_each_pagination(self, response):
        item = response.meta['item']                     
        for link in response.xpath('.//li[contains(@class,"box-product")]/a/@href'):
            url = link.extract()
            yield scrapy.Request(url, callback=self.parse_product, meta={'item': item})          

    def parse_product(self, response):
        item = response.meta['item']
        item['url'] = response.urljoin("")

        item['title'] = response.xpath('.//div[@class="product-name"]/h1/text()').extract_first()


        # image_url
        item['image_url'] = response.css('#image::attr(src)').extract_first()

        # price
        regular_price = response.xpath('.//span[contains(@class,"price") and contains(@class,"old-price")]/text()').extract_first()
        item['regular_price'] = re.sub('[^0-9.]', '', regular_price)
        sale_price = response.css('#price::text').extract_first()
        item['sale_price'] = re.sub('[^0-9.]', '', sale_price)
        yield item