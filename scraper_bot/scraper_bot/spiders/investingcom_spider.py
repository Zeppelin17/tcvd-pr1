import scrapy


class InvestingcomSpider(scrapy.Spider):
    name = "investingcom_spider"

    def __init__(self, equity: str, method: str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        base = f"https://www.investing.com/equities/{equity}"
        self.start_urls = [
            base if method == "current" else f"{base}-historical-data"
        ]
        self.method = method

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(
                url,
                callback=self.parse,
                errback=self.handle_error,
                dont_filter=True,
            )

    def handle_error(self, failure):
        yield {"error": str(failure)}

    def parse(self, response):

        if self.method == "current":
            yield from self.parse_current(response)
        else:
            yield {}

    def parse_current(self, response):
        stats = {}
        rows = response.css("div.key-info__table--value-pair")

        for row in rows:
            label = row.css("div.key-info__label::text").get()
            value = row.css("div.key-info__value::text").get()
            if label and value:
                stats[label.strip()] = value.strip()

        yield {"equity": response.url.split("/")[-1], "key_statistics": stats}
