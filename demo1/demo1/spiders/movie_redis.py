# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from demo1.items import Demo1Item


'''
第一次改动：添加
'''
from scrapy_redis.spiders import RedisCrawlSpider

'''
第二处改动： 继承 RedisCrawlSpider
        redis_key = 'nnspider:start_urls'

'''

class NnSpider(RedisCrawlSpider):
    name = 'movie'
    allowed_domains = ['www.id97.com']
    # start_urls = ['http://www.id97.com/movie/']
    redis_key = 'nnspider:start_urls'

    # 根据规则提取所有的页码链接
    page_link = LinkExtractor(allow=r'/movie/\?page=\d')
    detail_link = LinkExtractor(restrict_xpaths='//div[contains(@class,"col-xs-1-5")]/div/a')
    # follow : 是否跟进
    rules = (
        # 所有的页码不用处理，跟进即可
        Rule(page_link, follow=True),
        # 所有的详情页不用跟进
        Rule(detail_link, callback='parse_item', follow=False),
    )

    def parse_item(self, response):
        # 通过response的meta属性，获取到参数item
        item = Demo1Item()
        # 电影海报
        item['post'] = response.xpath('//a[@class="movie-post"]/img/@src').extract_first()
        # 电影名字
        item['name'] = response.xpath('//h1').xpath('string(.)').extract_first()
        # 电影评分
        item['score'] = response.xpath('//div[@class="col-xs-8"]/table/tbody/tr[last()]/td[2]').xpath('string(.)').extract_first()
        # 电影类型
        item['_type'] = response.xpath('//div[@class="col-xs-8"]/table/tbody/tr[3]/td[2]').xpath('string(.)').extract_first()
        # 导演
        item['director'] = response.xpath('//div[@class="col-xs-8"]/table/tbody/tr[1]/td[2]/a/text()').extract_first()
        # 编剧
        item['editor'] = response.xpath('//div[@class="col-xs-8"]/table/tbody/tr[2]/td[2]/a/text()').extract_first()
        # 主演
        # '张静初 / 龙品旭 / 黎兆丰 / 王同辉 / 张国强 / 叶婉娴 / 丽娜 / 吴海燕 / 吴若林 / 喻引娣 显示全部'
        item['actor'] = response.xpath('//div[@class="col-xs-8"]/table/tbody/tr[3]/td[2]').xpath('string(.)').extract_first().replace(' ', '').replace('显示全部', '')
        # 片长
        lala = response.xpath('//div[@class="col-xs-8"]/table/tbody/tr[8]/td[2]/text()').extract_first()
        if lala and ('分钟' in lala):
            item['long_time'] = lala
        else:
            item['long_time'] = ''
        # 电影介绍
        introduce = response.xpath('//div[@class="col-xs-12 movie-introduce"]').xpath('string(.)').extract_first()
        if introduce == None:
            item['introduce'] = ''
        else:
            item['introduce'] = introduce.replace('\u3000', '').replace('展开全部', '')
        # 电影链接
        # item['download_url'] = response.xpath('')
        yield item

