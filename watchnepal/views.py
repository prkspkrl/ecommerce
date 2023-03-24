from django.shortcuts import render
from homepage.models import Slider, Whyus
from store.models import Product
from category.models import Category
from blog.models import Blog

def home(request,category_slug=None):
    slider = Slider.objects.all()
    categories = Category.objects.all()
    new_product = Product.objects.filter(labels="new")
    why = Whyus.objects.all()
    blogs = Blog.objects.all()

    #category by product
    category_nf = Category.objects.get(slug='naviforce')
    product_by_category = Product.objects.filter(category__category_name=category_nf)
    # print(product_by_category)

    context = {

        'slider' : slider,
        'categories'  : categories,
        'new_product' : new_product,
        'why'         : why,
        'blogs'        : blogs,
        'cat_prod' : product_by_category,
    }
    return render(request,'home.html', context)