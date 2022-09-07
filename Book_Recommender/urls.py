"""Book_Recommender URL Configuration

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
from django.contrib import admin
from django.urls import path
from django.contrib.auth.models import User
from App import views
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import PasswordChangeView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('uploaddataset/',views.upload,name = "Upload dataset"),
     
    # consisting home module
    path('',views.allgenre),
    path('bookson/',views.bookongenre),
    path('about/',views.about),
    path('getbook/<int:id>/',views.search, name='search'),
    path('signup/',views.signup),
    path('login/',views.loginuser, name='login'),
    path('logout/',views.logouts, name='logouts'),
    path('book/',views.allbook),
    path('search_auto/', views.search_auto, name='search_auto'),

    # for image and password of user
    path('profile/',views.change_password_profile, name='profile'),
    path('updateprofile/',views.addprofile),
    path('updateImage/',views.updateImage),
    path('deleteimage/',views.deleteimage),

    #consisting genre or book module
    path('add_to_fav/<int:id>',views.add_fav,name="Add to favourite"),
    path('remove_from_fav/<int:id>',views.remove_fav,name="Remove from favourite"),
    path('user_fav/',views.get_user_fav,name='wishlist'),


    # To reset password
    path('password_reset/',auth_views.PasswordResetView.as_view(template_name='registration/reset_form_1.html'),name='password_reset'),
    path('password_reset/done/',auth_views.PasswordResetDoneView.as_view(template_name='registration/reset_done_3.html'),name='password_reset_done'),
    path('reset/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name='registration/reset_confirm_4.html'),name='password_reset_confirm'),
    path('reset/done/',auth_views.PasswordResetCompleteView.as_view(template_name='registration/reset_complete_5.html'),name='password_reset_complete'),

] 

# to link media folder to add/update profile to urls.py
urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)