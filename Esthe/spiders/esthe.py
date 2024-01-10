import scrapy
from ..items import EstheItem

class EstheSpider(scrapy.Spider):
    name = "esthe"
    allowed_domains = ["www.esthe.co.uk"]
    start_urls = ["https://www.esthe.co.uk/shop/"]

    def parse(self, response):
        products = response.xpath("//h2[@class='woocommerce-loop-product__title etheme-product-grid-title']/a/@href").getall()
        print("{} Product Link Found".format(len(products)))
        for product in products:
            yield scrapy.Request(product,callback=self.scrape_item)
        
        next_page = response.xpath("//a[@class='next page-numbers']/@href").get()
        yield scrapy.Request(next_page,callback=self.parse)
    
    def scrape_item(self,response):
        item = EstheItem()
        item["product_name"] = response.xpath("//h1[@class='product_title entry-title elementor-heading-title elementor-size-default']/text()").get(default="not-found")

        item["product_price"] = response.xpath("string(//p[@class='price']/ins)").getall()[0].strip()
        if item["product_price"] == '':
            item["product_price"] = response.xpath("string(//p[@class='price']/span/bdi)").getall()[0].strip()

        item["product_description"] = response.xpath("string(//div[@id='tab-description']/p)").getall()[0].strip()

        item["product_image_url"] = response.xpath("//a[@class='woocommerce-main-image pswp-main-image zoom']/@href").get(default="not-found")
        item["product_url"] = response.url
        yield item

