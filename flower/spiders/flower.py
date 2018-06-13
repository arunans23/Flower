# -*- coding: utf-8 -*-
import scrapy
import os
import re
from scrapy.selector import Selector


class FlowerSpider(scrapy.Spider):
    name = 'flower'
    allowed_domains = os.environ.get('allowed_domain')

    def start_requests(self):
        start_url = os.environ.get('crawl_url')
        yield scrapy.Request(url=start_url, callback=self.parse)
        for i in range(2,500):
            yield scrapy.Request(url=start_url + "&page=" + str(i) , callback=self.parse)

    def parse(self, response):
        sel = Selector(response)
        results = sel.select("//tr/td[@class='alt1']")
        for result in results:
            #filtering name posts
            # names = result.select('.//font[contains(@color, "Purple")]').extract()
            names = result.select('.//div[contains(text(),"{}")]'.format(os.environ.get('keyword1'))).extract()
            if(len(result.select(".//br"))>10 and len(names) == 0):
                story = result.extract()
                if os.environ.get('keyword2') in story:
                    re_exp_newline = re.compile('<br>\n<br>')
                    re_exp_remove_tag = re.compile('<.*?>')
                    story = re.sub(re_exp_newline, '\n', story)
                    story = re.sub(re_exp_remove_tag, '', story)
                    # story = re.sub(r'\n+', '\n',story)

                    story = re.sub(r'\n\s*\n', '\n\n', story)
                    story = re.sub(r'OA_show("postbit");', '', story)
                    page = re.sub('.*&+','',response.request.url)
                    if(len(page)>8):
                        page = "page=0"
                    print("*******************************************************")
                    story = re.sub('Last.*',"",story)
                    story = re.sub("The following+.*","",story)
                    with open('output.txt', 'a') as f:
                        f.write(page)
                        f.write(story)
                        f.write("\n                       **************************\n\n\n")
