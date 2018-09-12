from jieba.analyse import ChineseAnalyzer
from haystack.backends import whoosh_backend
from whoosh.fields import TEXT


class MyTEXT(TEXT):
    def __init__(self, *args, **kwargs):
        # 为中文分词，修改默认的分词器为结巴分词器
        kwargs['analyzer'] = ChineseAnalyzer()
        super().__init__(*args, **kwargs)


whoosh_backend.TEXT = MyTEXT
WhooshEngine = whoosh_backend.WhooshEngine