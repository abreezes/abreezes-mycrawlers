import demjson

class Parse:
    def __init__(self,parse_type=None):
        self.parse_type=parse_type

    def parses(self,html):
        if self.parse_type == 'get_comment_page':
            res=demjson.decode(html.strip()[11:-1])
            return res

        if self.parse_type == 'get_page':
            res=demjson.decode(html.strip()[20:-1])
            return res