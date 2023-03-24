from django.shortcuts import render
from .models import Blog

# Create your views here.

def blog(request):
    blogs = Blog.objects.all()
    month = blogs[0].created_date.strftime('%B')

    context = {
        'blogs':blogs,
        'month':month,
    }
    return render(request, 'blog/blog.html',context)


def blog_detail(request, blog_slug):
    try:
        blog_detail = Blog.objects.get(slug=blog_slug)

    except Exception as e:
        raise e

    context= {
        'blog': blog_detail,
    }

    return render(request,'blog/blog_detail.html', context)

