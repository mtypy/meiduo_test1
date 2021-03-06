import os
from collections import OrderedDict
from django.conf import settings

from contents.models import ContentCategory
from goods.models import GoodsChannel


def generate_static_index_html():
    """生成首页的静态页面index.html"""
    print('generate_static_index_html')

    # 1. 从数据库中查询出首页所需`商品分类`和`首页广告`
    # 商品分类
    # 使用有序字典保存类别的顺序
    # categories = {
    #     1: { # 组1
    #         'channels': [{'id':, 'name':, 'url':},{}, {}...],
    #         'sub_cats': [{'id':, 'name':, 'sub_cats':[{},{}]}, {}, {}, ..]
    #     },
    #     2: { # 组2
    #
    #     }
    # }
    categories = OrderedDict()
    channels = GoodsChannel.objects.order_by('group_id', 'sequence')
    for channel in channels:
        group_id = channel.group_id  # 当前组

        if group_id not in categories:
            categories[group_id] = {'channels': [], 'sub_cats': []}

        cat1 = channel.category  # 当前频道的类别

        # 追加当前频道
        categories[group_id]['channels'].append({
            'id': cat1.id,
            'name': cat1.name,
            'url': channel.url
        })
        # 构建当前类别的子类别
        for cat2 in cat1.goodscategory_set.all():
            cat2.sub_cats = []
            for cat3 in cat2.goodscategory_set.all():
                cat2.sub_cats.append(cat3)
            categories[group_id]['sub_cats'].append(cat2)

    # 广告内容
    contents = {}
    content_categories = ContentCategory.objects.all()
    for cat in content_categories:
        contents[cat.key] = cat.content_set.filter(status=True).order_by('sequence')

    # 2. 使用`index.html`模板文件，进行模板渲染，获取渲染之后html页面内容
    context = {
        'categories': categories,
        'contents': contents
    }

    # 加载模板：指定使用的模板文件，获取一个模板对象
    from django.template import loader
    temp = loader.get_template('index.html')

    # 模板渲染：给模板文件传递数据，替换模板变量，获取替换之后html页面内容
    res_html = temp.render(context)

    # 3. 将渲染之后html页面内容保存成一个静态页面
    save_path = os.path.join(settings.GENERATED_STATIC_HTML_FILES_DIR, 'index.html')

    with open(save_path, 'w', encoding='utf-8') as f:
        f.write(res_html)

