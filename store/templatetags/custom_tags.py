from django import template
from .. models import *

register = template.Library()
cata= Product.objects.all()
chata=OrderItem.objects.all()
@register.simple_tag

def total_price(price,quantity):
    return price*quantity
  