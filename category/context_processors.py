from .models import Category
from store.models import Product


#Context processors will aaileble all the files of Django thats why i use it. and register in setting.py
def menu_links(request):
    links = Category.objects.all()


    #for count of product in categories not fixed
    product_cat = Product.objects.filter(category__id__in=links)
    link_count = product_cat.count()

    # print(link_count)
    return dict(links=links, link_count = link_count)


