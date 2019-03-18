import logging
import time

from scrapy.dupefilters import BaseDupeFilter
from .custom_request import request_fingerprint
# from scrapy.utils.request import request_fingerprint

from . import defaults
from .connection import get_redis_from_settings

#####################bloomfilter(1)#############################
# isUseBloomfilter = False
# try:
#     from .Bloomfilter import BloomFilter
# except Exception as e:
#     print(f"there is no BloomFilter, used the default redis set to dupefilter.")
# else:
#     isUseBloomfilter = True

#####################bloomfilter(2)#############################
from .py_bloomfilter import PyBloomFilter,conn

logger = logging.getLogger(__name__)


# TODO: Rename class to RedisDupeFilter.
class RFPDupeFilter(BaseDupeFilter):
    """Redis-based request duplicates filter.

    This class can also be used with default Scrapy's scheduler.

    """

    logger = logger

    def __init__(self, server, key, debug=False):
        """Initialize the duplicates filter.

        Parameters
        ----------
        server : redis.StrictRedis
            The redis server instance.
        key : str
            Redis key Where to store fingerprints.
        debug : bool, optional
            Whether to log filtered requests.

        """
        self.server = server
        self.key = key
        self.debug = debug
        self.logdupes = True
        self.bf = PyBloomFilter(conn=conn,key=self.key)

        #####################bloomfilter(1)#############################
        # 使用 Bloonfilter 来对url去重
        # if isUseBloomfilter == True:
        #     self.bf = BloomFilter()

    @classmethod
    def from_settings(cls, settings):
        """Returns an instance from given settings.

        This uses by default the key ``dupefilter:<timestamp>``. When using the
        ``scrapy_redis.scheduler.Scheduler`` class, this method is not used as
        it needs to pass the spider name in the key.

        Parameters
        ----------
        settings : scrapy.settings.Settings

        Returns
        -------
        RFPDupeFilter
            A RFPDupeFilter instance.


        """
        server = get_redis_from_settings(settings)
        # XXX: This creates one-time key. needed to support to use this
        # class as standalone dupefilter with scrapy's default scheduler
        # if scrapy passes spider on open() method this wouldn't be needed
        # TODO: Use SCRAPY_JOB env as default and fallback to timestamp.
        key = defaults.DUPEFILTER_KEY % {'timestamp': int(time.time())}
        debug = settings.getbool('DUPEFILTER_DEBUG')
        return cls(server, key=key, debug=debug)

    @classmethod
    def from_crawler(cls, crawler):
        """Returns instance from crawler.

        Parameters
        ----------
        crawler : scrapy.crawler.Crawler

        Returns
        -------
        RFPDupeFilter
            Instance of RFPDupeFilter.

        """
        return cls.from_settings(crawler.settings)

    def request_seen(self, request):
        """Returns True if request was already seen.

        Parameters
        ----------
        request : scrapy.http.Request

        Returns
        -------
        bool

        """
        #####################bloomfilter(1)#############################
        # if isUseBloomfilter == True:
        #     # 使用 Bloomfilter 来对url去重
        #     fp = self.request_fingerprint(request)
        #     if self.bf.isContains(fp):  # 如果已经存在
        #         return True
        #     else:
        #         self.bf.insert(fp)
        #         return False
        # else:
        #     # 使用redis默认的set进行去重
        #     fp = self.request_fingerprint(request)
        #     # This returns the number of values added, zero if already exists.
        #     added = self.server.sadd(self.key, fp)
        #     return added == 0
        #####################bloomfilter(2)#############################

        fp = self.request_fingerprint(request)
        #集成boolmfiter,判断是否存在
        if self.bf.is_exist(fp):
            return True
        else:
            self.bf.add(fp)
            return False

        #####################源代码#############################
        # fp = self.request_fingerprint(request)
        # # This returns the number of values added, zero if already exists.
        # added = self.server.sadd(self.key, fp)
        # return added == 0

    def request_fingerprint(self, request):
        """Returns a fingerprint for a given request.

        Parameters
        ----------
        request : scrapy.http.Request

        Returns
        -------
        str

        """
        return request_fingerprint(request)

    def close(self, reason=''):
        """Delete data on close. Called by Scrapy's scheduler.

        Parameters
        ----------
        reason : str, optional

        """
        self.clear()

    def clear(self):
        """Clears fingerprints data."""
        self.server.delete(self.key)

    def log(self, request, spider):
        """Logs given request.

        Parameters
        ----------
        request : scrapy.http.Request
        spider : scrapy.spiders.Spider

        """
        if self.debug:
            msg = "Filtered duplicate request: %(request)s"
            self.logger.debug(msg, {'request': request}, extra={'spider': spider})
        elif self.logdupes:
            msg = ("Filtered duplicate request %(request)s"
                   " - no more duplicates will be shown"
                   " (see DUPEFILTER_DEBUG to show all duplicates)")
            self.logger.debug(msg, {'request': request}, extra={'spider': spider})
            self.logdupes = False