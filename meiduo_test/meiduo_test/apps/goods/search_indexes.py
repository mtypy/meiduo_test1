# 定义商品的索引类
from haystack import indexes
from goods.models import SKU

# BookInfo


# 索引类名字格式: 模型类+Index
class SKUIndex(indexes.SearchIndex, indexes.Indexable):
    # document=True说明这个字段是索引字段
    # use_template=True说明建立索引数据时，索引字段包含哪些内容会在一个文件中进行指定
    text = indexes.CharField(document=True, use_template=True)

    def get_model(self):
        """返回索引类对应模型类"""
        return SKU

    def index_queryset(self, using=None):
        """返回需要建立索引数据的查询集"""
        return self.get_model().objects.filter(is_launched=True)