from rest_framework.pagination import PageNumberPagination


class StandardResultPagination(PageNumberPagination):
    """自定义分页类"""
    # 分页默认页容量
    page_size = 2
    # 获取分页数据时页容量参数的名称
    page_size_query_param = 'page_size'
    # 最大页容量
    max_page_size = 20
