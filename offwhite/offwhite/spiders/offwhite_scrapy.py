import scrapy
from ..items import OffwhiteItem

class OffWhiteScrapy(scrapy.Spider):
    name = 'ow'
    root = 'https://www.off---white.com'
    start_urls = ['https://www.off---white.com/en/US/women/t/seasons/fw2018']
    # headers = {'Connection':'keep-alive', 'User-Agent:':'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:61.0) Gecko/20100101 Firefox/61.0'}
    headers = {'Connection':'keep-alive', 'User-Agent:':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'}

    def parse(self, response):
        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.list_item, headers=self.headers)

    def list_item(self, response):
        list_url = response.xpath('//article[@class="product"]/a/@href').extract()[:3]
        print("List URL : %s" % list_url)
        for url in list_url:
            yield scrapy.Request(url=self.root + url, callback=self.item_parse, headers=self.headers )

    def item_parse(self, response):
        item = OffwhiteItem()

        item['description'] = ''.join(self.get_description(response))
        item['title'] = self.get_title(response)[0].strip()
        item['price'] = self.get_price(response)[0]
        item['size'] = self.get_size(response)
        item['images'] = self.get_images(response)

        yield item

    def get_description(self, response):
        return response.xpath('//div[@class="product-description"]/p[@id="details"]/@content').extract()

    def get_title(self, response):
        return response.xpath('//span[@class="prod-title"]/text()').extract()

    def get_price(self, response):
        return response.xpath('//div[@class="price"]/span[@itemprop="price"]/@content').extract()

    def get_size(self, response):
        return response.xpath('//div[@class="styled-radio"]/label/text()').extract()

    def get_images(self, response):
        return response.xpath('//div[@class="container-images"]/img/@src').extract()