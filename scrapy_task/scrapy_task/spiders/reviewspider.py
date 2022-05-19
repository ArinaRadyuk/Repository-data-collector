from datetime import datetime
import scrapy
from ..items import (ReleaseInfo, GithubItem, CommitInfo)


class ReviewSpider(scrapy.Spider):
    name = 'reviewspider'
    allowed_domains = ['github.com']

    def __init__(self, *args, **kwargs):
        super(ReviewSpider, self).__init__(*args, **kwargs)
        self.start_urls = kwargs.get('start_urls').split(',')

    @staticmethod
    def follow_link(link, func, repo_id, field):
        if link is not None:
            link = "https://github.com" + link
            yield scrapy.Request(url=link, callback=func, meta={"id": repo_id})
        else:
            yield {field: None, "repo_id": repo_id}

    @staticmethod
    def get_time(response):
        local_time = response.xpath("//local-time[@class='no-wrap']/@datetime").get()
        relative_time = response.xpath("//relative-time[@class='no-wrap']/@datetime").get()
        if local_time is None:
            time = relative_time
        else:
            time = local_time
        x = datetime.strptime(time, "%Y-%m-%dT%H:%M:%S%z")
        return x.strftime("%c")

    def get_commit_info(self, response):
        commit_obj = CommitInfo(
            author=response.xpath("//*[@class='commit-author user-mention']/text()").get(),
            name=' '.join(response.xpath("//p")[0].xpath('a/text()').getall()),
            datetime=self.get_time(response)
        )
        yield {"last_commit": commit_obj, "repo_id": response.meta.get("id")}

    def get_release_info(self, response):
        release_obj = ReleaseInfo(
            version=response.xpath("//h1[@class='d-inline mr-3']/text()").get(),
            time=self.get_time(response),
            changelog=response.url
        )
        yield {"last_release": release_obj, "repo_id": response.meta.get("id")}

    def get_github_obj(self, link):
        github_obj = GithubItem(
            _id=link.xpath("//meta[@name='octolytics-dimension-repository_id']/@content").get(),
            name=link.xpath("//strong[@class='mr-2 flex-self-stretch']/a/text()").get(),
            description=link.xpath("normalize-space(//p[@class='f4 mb-3'])").get(),
            link=link.url,
            star=link.css('a:contains(star) strong::text').get(),
            fork=link.css('a:contains(fork) strong::text').get(),
            watching=link.css('a:contains(watching) strong::text').get(),
            commit=link.css('span:contains(commit) strong::text').get(),
            release=link.css('a:contains(Release) span::text').get())
        yield github_obj

        link_last_release = link.xpath("//a[@class='Link--primary d-flex no-underline']/@href").get()
        yield from self.follow_link(link_last_release, self.get_release_info, github_obj._id, "last_release")

        link_last_commit = link.xpath("//li[@class='ml-0 ml-md-3']/a/@href").get()
        yield from self.follow_link(link_last_commit, self.get_commit_info, github_obj._id, "last_commit")

    def parse(self, response):
        view_all = response.xpath("//a[@class='Link--muted text-bold']/@href").get()
        if view_all is not None:
            yield scrapy.Request(response.urljoin(view_all), callback=self.parse)
        author_page_links = response.xpath("//a[@class='d-inline-block']/@href").getall()
        for link in author_page_links:
            link = "https://github.com" + link
            yield scrapy.Request(link, callback=self.get_github_obj)

        next_page = response.xpath("//a[@class='next_page']/@href").get()
        if next_page is not None:
            next_page = "https://github.com" + next_page
            yield scrapy.Request(next_page, callback=self.parse)

# scrapy crawl reviewspider -a start_urls="https://github.com/scrapy,https://github.com/celery/"