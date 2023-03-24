from django.contrib import admin
from django.urls import path,include
from . import views

# for image show
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name= 'home'),
    path('store/', include('store.urls')),
    path('accounts/', include('accounts.urls')),
    path('category', include('category.urls')),
    path('contact/', include('contact.urls')),
    path('blog/', include('blog.urls')),
    path('cart/', include('carts.urls')),
    path('orders/', include('orders.urls')),
    # ---------------API---------------------
    path('api/', include('store.api_urls')),
    path('category/', include('category.api_urls')),
    # path('category/category-filter/', include('category.api_urls')),
    # path('category/category-crud/', include('category.api_urls')),



] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)