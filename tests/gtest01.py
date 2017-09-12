from pytdx.hq import TdxHq_API
api = TdxHq_API()
if api.connect('119.147.212.81', 7709):
    # ... same codes...
    data = api.get_security_bars(9, 0, '000001', 0, 10)  # 返回普通list
   # data= api.get_security_quotes([(0, '000001'), (1, '600300')])
   # data =api.get_security_bars(0, 0, "000001", 0, Count, Result, ErrInfo)
    print(data)
api.disconnect()