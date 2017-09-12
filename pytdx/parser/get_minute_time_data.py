# coding=utf-8

from pytdx.parser.base import BaseParser
from pytdx.helper import get_datetime, get_volume, get_price
from collections import OrderedDict
import struct
import six

"""
/// <summary>
/// 获取分时数据
/// </summary>
/// <param name="Market">市场代码,   0->深圳     1->上海</param>
/// <param name="Zqdm">证券代码</param>
/// <param name="Result">此API执行返回后，Result内保存了返回的查询数据, 形式为表格数据，行数据之间通过\n字符分割，列数据之间通过\t分隔。一般要分配1024*1024字节的空间。出错时为空字符串。</param>
/// <param name="ErrInfo">此API执行返回后，如果出错，保存了错误信息说明。一般要分配256字节的空间。没出错时为空字符串。</param>
/// <returns>成功返货true, 失败返回false</returns>
"""
"""
6 : 查询分时行情

参数：市场代码， 股票代码， 如： 0,000001 或 1,600300+

api.get_minute_time_data(1, '600300')
"""
class GetMinuteTimeData(BaseParser):

    def setParams(self, market, code):
        if type(code) is six.text_type:
            code = code.encode("utf-8")
        pkg = bytearray.fromhex(u'0c 1b 08 00 01 01 0e 00 0e 00 1d 05')
        pkg.extend(struct.pack("<H6sI", market, code, 0))
        self.send_pkg = pkg

    """
    b1cb74000c1b080001b61d05be03be03f0000000a208ce038d2c028302972f4124b11a00219821011183180014891c0009be0b4207b11000429c2041....

    In [26]: get_price(b, 0)
Out[26]: (0, 1)

In [27]: get_price(b, 1)
Out[27]: (0, 2)

In [28]: get_price(b, 2)
Out[28]: (546, 4)

In [29]: get_price(b, 4)
Out[29]: (-206, 6)

In [30]: get_price(b, 6)
Out[30]: (2829, 8)

In [31]: get_price(b, 8)
Out[31]: (2, 9)

In [32]: get_price(b, 9)
Out[32]: (131, 11)

In [36]: get_price(b, 11)
Out[36]: (3031, 13)

In [37]: get_price(b, 13)
Out[37]: (-1, 14)

In [38]: get_price(b, 14)
Out[38]: (36, 15)

In [39]: get_price(b, 15)
Out[39]: (1713, 17)

In [40]: get_price(b, 17)
Out[40]: (0, 18)
    """
    def parseResponse(self, body_buf):
        pos = 0
        (num, ) = struct.unpack("<H", body_buf[:2])
        last_price = 0
        pos += 4
        prices = []
        for i in range(num):
            price_raw, pos = get_price(body_buf, pos)
            reversed1, pos = get_price(body_buf, pos)
            vol, pos = get_price(body_buf, pos)
            last_price = last_price + price_raw
            price = OrderedDict(
                [
                    ("price", float(last_price)/100),
                    ("vol", vol)
                ]
            )
            prices.append(price)
        return prices
