from django import template
import math
register=template.Library()



@register.simple_tag
def cal_sellprice(price,offer):
    if offer is None or offer is 0:
        return price
    sellprice=price
    sellprice=price-( price * offer * 0.01)
    return math.floor(sellprice)    