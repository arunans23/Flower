# -*- coding: utf-8 -*-
import scrapy
import os
from scrapy.selector import Selector


class FlowerSpider(scrapy.Spider):
    name = 'flower'
    allowed_domains = os.environ.get('allowed_domain')

    def start_requests(self):
        start_url = os.environ.get('crawl_url')
        yield scrapy.Request(url=start_url, callback=self.parse)
        for i in range(2,500):
            yield scrapy.Request(url=start_url + "&page=" + str(i) , callback=self.parse)

    def test(self, result):
        results1 = result.select("//br")
        print(len(results1))

    def parse(self, response):
        sel = Selector(response)
        results = sel.select("//b")
        for result in results:
            #filtering name posts
            names = result.select('.//font[contains(@color, "Purple")]').extract()
            if(len(result.select(".//br"))>25 and len(names) == 0):
                story = result.extract()
                print("*******************************************************")
                
                with open('/home/isham/log2.txt', 'a') as f:
                    f.write(story)
                    
