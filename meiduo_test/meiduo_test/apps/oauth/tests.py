from urllib.parse import urlencode, parse_qs
from urllib.request import urlopen

from django.test import TestCase

# Create your tests here.
if __name__ == '__main__':
    #  urlopen(url) : 发起http网络请球
    req_url = "http://api.meiduo.site:8000/mobiles/13155667788/count/"
    # 发起http网络请求
    response = urlopen(req_url)

    # 获取响应数据
    res_data = response.read().decode()
    print(res_data)

# 将查询字符串转换为字典
# if __name__ == '__main__':
#     # parse_qs(qs): 将查询字符串转换为字典
#     qs = "b=2&a=1&c=3"
#     res = parse_qs(qs)
#     print(res)
#     #  运行结果{'c': ['3'], 'b': ['2'], 'a': ['1']}
#     # 注意：转换为字段 key对应的value对应的类型是；list

# 将字典转换为查询字符串
# if __name__ == '__main__':
#     # urlencode(dict) 将字典转换为查询字符串
#     data = {
#         "a": 1,
#         "b": 2,
#         "c": 3,
#
#     }
#     res = urlencode(data)
#     print(res)
#  运行结果 b=2&a=1&c=3
