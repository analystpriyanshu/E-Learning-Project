from django.contrib import admin
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
urlpatterns = [
path('admin/', admin.site.urls),
path('',views.indexpage,name='indexpage'),
path('indexpage2/<str:slug>',views.indexpage2,name='indexpage2'),
path('indexpage3/<str:slug>',views.indexpage3,name='indexpage3'),
path('verify_payment',views.verify_payment,name='verify_payment'),
path('about',views.about,name='about'),
path('gallery',views.gallery,name='gallery'),
path('address',views.address,name='address'),
path('signup',views.signup,name='signup'),
path('form',views.form,name='form'),
path('mycourses',views.mycourses,name='mycourses'),
path('logout',views.logout,name='logout'),
path('profile',views.profile,name='profile'),
path('edit',views.edit,name='edit'),
path('test',views.test,name='test'),
path('certificate',views.certificate,name='certificate'),
path('uploadsolution',views.uploadsolution,name='uploadsolution'),
path('reset_password/',
     auth_views.PasswordResetView.as_view(template_name="password_reset.html"),
     name="reset_password"),

    path('reset_password_sent/', 
        auth_views.PasswordResetDoneView.as_view(template_name="password_reset_done.html"), 
        name="password_reset_done"),

    path('reset/<uidb64>/<token>/',
     auth_views.PasswordResetConfirmView.as_view(template_name="password_reset_confirm.html"), 
     name="password_reset_confirm"),

    path('reset_password_complete/', 
        auth_views.PasswordResetCompleteView.as_view(template_name="password_reset_complete.html"), 
        name="password_reset_complete"),
]
