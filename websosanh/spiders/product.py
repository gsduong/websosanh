import scrapy
from websosanh.items import LazadaItem

class LazadaSpider(scrapy.Spider):
    name = "lazada"
    allowed_domains = ["lazada.vn"]
    start_urls = ["http://www.lazada.vn/"]

    def parse(self, response): # looking for links of parent categories
        nav_wrapper = response.xpath('.//*[@class="c-second-menu__item c-second-menu__item_style_heading2"]/a/@href')
        # Remove duplicate
        links = []
        for i in nav_wrapper:
            if str(i.extract()) not in links:
                links.append(str(i.extract()))

        links.pop() # Remove last item for error solving
        for url in links:
            yield scrapy.Request(url, callback=self.parse_all_pagination)   # each url is a link to a parent category, each category has many paginations


    def parse_all_pagination(self, response):

        nav_pagination = response.css("div.c-paging__wrapper > a::text")

        page_number = []

        for i in nav_pagination: # get number of pages paginated
            j = int(i.extract()) # convert unicode to integer
            if j not in page_number:
                page_number.append(j)
        pagination_links = [response.urljoin("?page=")+`page` for page in range(min(page_number), max(page_number) + 1)]

        for url in pagination_links:
            yield scrapy.Request(url, callback=self.parse_each_pagination)  # each pagination has many products

    def parse_each_pagination(self, response):                              # get links of all product in each pagination
        for item in response.xpath('.//div[@class="product-card__name-wrap"]/span/text()'):
            product = LazadaItem()
            product['title'] = item.extract()
            yield product
            #yield scrapy.Request(url, callback=self.parse_product)          # call a callback to parse product in each product link

    # def parse_product(self, response):
    #     item = LazadaItem()

    #     item['item_link'] = response.url
    #     item['image_link'] = response.xpath('//*[@id="scj_product_detail"]//img[@id="scjZoom"]/@src').extract()
        # item['description'] = response.xpath('//div[@class="info_wrap"]/*').extract()
        # yield item