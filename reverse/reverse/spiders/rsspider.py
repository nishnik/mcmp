from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from reverse.items import ReverseItem
from scrapy.http import Request
import pickle
import re



# class MySpider(Spider):
#     """
#     Scrapy code for scraping the list of all departments and schools :
#     Usage:
#     scrapy crawl reverse -o departments.json -t json
#     """
#
#     name = "reverse"
#     allowed_domains = ["www.iitkgp.ac.in"]
#     start_urls = ["http://www.iitkgp.ac.in/commdir3/various.php?division=3"]
#
#     def parse(self, response):
#         sel = Selector(response)
#         titles = sel.xpath('//*/table')
#         item = ReverseItem()
#         item["title"] = titles.xpath('.//*/a/@href').extract()
#         item["field"] = titles.xpath('.//*/a/text()').extract()
#
#         return item
#
#
# class MySpider(Spider):
#     """
#     Scrapy code for scraping the list of all professors from various departments
#     Usage
#     scrapy crawl reverse -o professor.json -t json
#
#     """
#     name = "reverse"
#     allowed_domains = ["www.iitkgp.ac.in"]
#     deplinks = open("deplinks.pkl", 'rb')
#
#     start_urls = pickle.load(deplinks)
#
#     def parse(self, response):
#         sel = Selector(response)
#         titles = sel.xpath('//*/table')
#         item = ReverseItem()
#         items = []
#
#         for title in titles:
#             item["title"] = title.xpath('.//*/a/@href').extract()
#             item["field"] = title.xpath('.//*/a/text()').extract()
#             items.append(item)
#         return items


class MySpider(BaseSpider):
    """
    Scrapy code for scraping the research areas of the various professors
    Usage :
    scrapy crawl reverse -o research_areas.json -t json
    """

    name = "reverse"
    allowed_domains = ["www.iitkgp.ac.in"]
    proflinks = open("proflinks.pkl", 'rb')

    start_urls = pickle.load(proflinks)
    items = []

    def parse(self, response):

        sel = HtmlXPathSelector(response)
        titles = sel.select('//*[@id="contents"]/fieldset')
        items = []
        item = ReverseItem()
        item["title"] = response.url
        item["field"] = titles[2].select('.//ul/li/text()').extract()
	image = sel.select('.//@src').extract()[-1] # luckily the last image is the one we need
        item["image"] = "http://www.iitkgp.ac.in" + image
        header_txt = titles[0].select("string((.//table/tr/td[2]))")[0].extract()
        re_year = re.compile('\d{4,4}')  # Match four digits
        re_dept = re.compile('Professor,[\s\w&]*')
        item["year"] = re_year.findall(header_txt)[0]
        item["dept"] = re_dept.findall(header_txt)[0].split('\n')[0].lstrip('Professor,').lstrip().rstrip()

        name = str((titles[0].select("string((.//table/tr/td[2]//text())[1])").extract())[0])
        item["name"] = name.lstrip().rstrip()
        items.append(item)
        return items
