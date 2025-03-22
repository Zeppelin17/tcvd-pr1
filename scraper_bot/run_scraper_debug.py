import os
import sys
from scrapy.cmdline import execute

# Establecer el entorno para que Scrapy encuentre el proyecto
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault("SCRAPY_SETTINGS_MODULE", "scraper_bot.settings")

execute(
    [
        "scrapy",
        "crawl",
        "investingcom_spider",
        "-a",
        "equity=apple-computer-inc",
        "-a",
        "method=current",
    ]
)
