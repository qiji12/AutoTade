# coding=utf-8

from pytdx.parser.base import BaseParser
from pytdx.helper import get_datetime, get_volume, get_price
from collections import OrderedDict
import struct

"""
1: 获取市场代码

可以获取该api服务器可以使用的市场列表，类别等信息
api.get_markets()
返回结果 api.to_df(api.get_markets()) 一般某个服务器返回的类型比较固定，该结果可以缓存到本地或者内存中。
2017-07-31 21:22:06,067 - PYTDX - INFO - 获取市场代码
    market  category    name short_name
0        1         1     临时股         TP
1        4        12  郑州商品期权         OZ
2        5        12  大连商品期权         OD
3        6        12  上海商品期权         OS
4        8        12  上海个股期权         QQ
5       27         5    香港指数         FH
6       28         3    郑州商品         QZ
7       29         3    大连商品         QD
8       30         3    上海期货         QS
9       31         2    香港主板         KH
10      32         2    香港权证         KR
11      33         8   开放式基金         FU
12      34         9   货币型基金         FB
13      35         8  招商理财产品         LC
14      36         9  招商货币产品         LB
15      37        11    国际指数         FW
16      38        10  国内宏观指标         HG
17      40        11   中国概念股         CH
18      41        11  美股知名公司         MG
19      43         1   B股转H股         HB
20      44         1    股份转让         SB
21      47         3    股指期货         CZ
22      48         2   香港创业板         KG
23      49         2  香港信托基金         KT
24      54         6   国债预发行         GY
25      60         3  主力期货合约         MA
26      62         5    中证指数         ZZ
27      71         2     港股通         GH
"""

class GetMarkets(BaseParser):

    def setup(self):
        self.send_pkg = bytearray.fromhex("01 02 48 69 00 01 02 00 02 00 f4 23")

    def parseResponse(self, body_buf):

        pos = 0
        (cnt, ) = struct.unpack("<H", body_buf[pos: pos + 2])
        pos += 2

        result = []
        for i in range(cnt):
            # 64byte for one
            (category, raw_name, market, raw_short_name, _, unknown_bytes) = struct.unpack("<B32sB2s26s2s", body_buf[pos: pos+64])
            pos += 64

            if category == 0 and market == 0:
                continue

            name = raw_name.decode("gbk")
            short_name = raw_short_name.decode("gbk")

            result.append(OrderedDict(
                [
                    ("market", market),
                    ("category", category),
                    ("name", name.rstrip("\x00")),
                    ("short_name", short_name.rstrip("\x00")),
                    #('unknown_bytes', unknown_bytes)
                ]
            ))

        return result


