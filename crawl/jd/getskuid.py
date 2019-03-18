
import downloads,parses

class GetSKUId:
    base_url = 'http://so.m.jd.com/ware/search._m2wq_list?keyword=macbook&datatype=1&callback=jdSearchResultBkCbA&page={}&pagesize=10&ext_attr=no&brand_col=no&price_col=no&color_col=no&size_col=no&ext_attr_sort=no&merge_sku=yes&multi_suppliers=yes&area_ids=1,72,2819&qp_disable=no&fdesc=%E5%8C%97%E4%BA%AC'

    def __init__(self):
        self.download = downloads.Downlaod()
        self.parse=parses.Parse(parse_type='get_page')

    @property
    def get_skuid(self):
        """获取商品的skuid"""
        url_list=self.genrate_url
        for url in url_list:
            html=self.download.download(url)
            res=self.parse.parses(html)
            shops=res['data']['searchm']['Paragraph']
            for shop in shops:
                yield shop['wareid']

    # @property
    # def get_page_count(cls,page=1):
    #     """获取总页码"""
    #     url=cls.base_url.format(page)
    #     html = cls.download.download(url)
    #     res = cls.parse.parses(html)
    #     pages = res['data']['searchm']['Head']['Summary']['Page']['PageCount']
    #     return pages

    @property
    def genrate_url(cls):
        """生成总的url列表"""
        # return [cls.base_url.format(page) for page in range(1, int(cls.get_page_count))]
        return [cls.base_url.format(page) for page in range(1,50 )]



if __name__ == '__main__':
    g=GetSKUId()
    for i in g.get_skuid:
        print(i)