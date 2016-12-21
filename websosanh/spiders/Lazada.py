import scrapy
from websosanh.items import LazadaItem

class LazadaSpider(scrapy.Spider):
    name = "lazada_spider"
    allowed_domains = ["lazada.vn"]
    start_urls = [
        "http://www.lazada.vn/dien-thoai-di-dong/",
        "http://www.lazada.vn/may-tinh-bang/",
        "http://www.lazada.vn/laptop/",
        "http://www.lazada.vn/may-tinh-de-ban-va-phu-kien/"
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
        item = LazadaItem()
        category_dict = {
            "http://www.lazada.vn/dien-thoai-di-dong/": 'cellphone',
            "http://www.lazada.vn/may-tinh-bang/": 'tablet',
            "http://www.lazada.vn/laptop/": 'laptop',
            "http://www.lazada.vn/may-tinh-de-ban-va-phu-kien/": 'desktop'
        }

        nav_pagination = response.css("div.c-paging__wrapper > a::text") 
        page_number = []
        category_url = response.urljoin("")

        item['category'] = category_dict[category_url]

        for i in nav_pagination: # get number of pages paginated
            j = int(i.extract()) # convert unicode to integer
            if j not in page_number:
                page_number.append(j)
        pagination_links = [response.urljoin("?page=")+`page` for page in range(min(page_number), max(page_number) + 1)]

        for url in pagination_links:
            yield scrapy.Request(url, callback=self.parse_each_pagination, meta={'item': item})

    def parse_each_pagination(self, response):
        item = response.meta['item']                     
        for page in response.xpath('.//div[contains(@class,"product-card")]/a/@href'):
            url = page.extract()
            yield scrapy.Request(url, callback=self.parse_product, meta={'item': item})          

    def parse_product(self, response):
        item = response.meta['item']
        item['url'] = response.urljoin("")

        item['title'] = response.xpath('.//title/text()').extract_first()


        # image_url
        res = response.css('#productImageBox')
        res = res.xpath('.//ul/li/div/div')[0]
        res = res.xpath('.//@data-swap-image')
        item['image_url'] = res.extract_first()

        # price
        item['sale_price'] = str(response.css('#special_price_box::text').extract_first())
        item['product_saving'] = str(response.css('#product_saving_percentage::text').extract_first())
        item['regular_price'] = str(response.css('#price_box::text').extract_first()).replace(" VND,", "")
        yield item