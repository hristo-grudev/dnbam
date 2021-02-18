import scrapy

from scrapy.loader import ItemLoader
from ..items import DnbamItem
from itemloaders.processors import TakeFirst


class DnbamSpider(scrapy.Spider):
	name = 'dnbam'
	start_urls = ['https://dnbam.com/en/news']

	def parse(self, response):
		post_links = response.xpath('//div[@class="block block-news"]/a/@href').getall()
		yield from response.follow_all(post_links, self.parse_post)

	def parse_post(self, response):
		title = response.xpath('//h1/text()').get()
		description = response.xpath('//div[contains(@class, "content")]//text()[normalize-space() and not(ancestor::div[contains(@class, "footer")] | ancestor::h4[@data-animate] | ancestor::h1)]').getall()
		description = [p.strip() for p in description]
		description = ' '.join(description).strip()
		date = response.xpath('//time/text()').get()

		item = ItemLoader(item=DnbamItem(), response=response)
		item.default_output_processor = TakeFirst()
		item.add_value('title', title)
		item.add_value('description', description)
		item.add_value('date', date)

		return item.load_item()
