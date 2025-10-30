"""mainproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls import handler400, handler403, handler404, handler500
from django.conf.urls.static import static
from django.contrib import admin, sitemaps
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from django.contrib.sitemaps.views import sitemap
from django.urls import path, include, re_path
from accounts.views import account, edit_account, address,recent_order, logout_page,contact, home, privacy_policy, refund_policy, robots_txt, terms, videos, customhandler404, customhandler403, customhandler500, RequestRefund, downloads, toggle_maintenance, maintenance_switch
from blog.sitemaps import CategorySitemaps, PostSitemaps, CommentSiteMaps, AuthorSitemaps
from accounts.sitemaps import StaticViewSitmap
from store.sitemaps import productSitmaps
sitemaps = {'static': StaticViewSitmap, 'posts': PostSitemaps, 'comments': CommentSiteMaps, 'categories':CategorySitemaps, 'authors': AuthorSitemaps, 'products': productSitmaps}


urlpatterns = [
    path('sitemap.xml/', sitemap, {'sitemaps': sitemaps}),
    path('robots.txt/', robots_txt,  name='robots.txt'),
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('api/', include('rest_framework.urls')),
    path('contact/', contact, name='contact'),
    path('privacy-policy/', privacy_policy, name='privacy'),
    path('refund-policy', refund_policy, name='refund'),
    path('terms/', terms, name='terms'),
    path('videos/', videos, name='videos'),
    path('logout/', logout_page, name='logout'),
    path('reset_password', auth_views.PasswordResetView.as_view(template_name='password_reset.html'), name='reset_password'),
    path('reset_password_sent', auth_views.PasswordResetDoneView.as_view(template_name='password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset_password_complete', auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'), name='password_reset_complete'),
    path('accounts/', include('allauth.urls')),
    path('my-account/', account, name='my_account'),
    path('my-account/edit-account/', edit_account, name='edit_account'),
    path('my-account/edit-billing-address/', address, name='address'),
    path('my-account/downloads/', downloads, name='downloads'),
    path('my-account/orders/', recent_order, name='orders'),
    path('my-account/request-refund/', login_required(RequestRefund.as_view()) , name='request_refund'),
    path('toggle-maintenance/', toggle_maintenance, name='toggle_maintenance'),
     path('maintenance-switch/', maintenance_switch), 
    re_path(r"^maintenance-mode/", include("maintenance_mode.urls")),
    path('', include('store.urls')),
    path('', include('newsletter.urls')),
    path('', include('blog.urls')),
] + static(settings.MEDIA_URL, document_root= settings.MEDIA_ROOT)

handler404 = customhandler404
handler500 = customhandler500
handler403 = customhandler403