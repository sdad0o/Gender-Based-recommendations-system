from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_view
from .forms import LoginForm,MyPasswordResetForm,PasswordChangeForm
urlpatterns = [
    path('',views.home),
    path('', views.CustomLoginView.as_view(template_name='app/login.html', authentication_form=LoginForm, next_page='index'), name='login'),
    path('contactUs/',views.contactUs ,name='contactUs'),
    path('aboutUs/',views.aboutUs ,name='aboutUs'),
    path('Mtime/',views.Mtime ,name='Mtime'),
    path('Ftime/',views.Ftime ,name='Ftime'),
    path('category/<slug:val>' ,views.CategoryView.as_view(), name='category'),
    path('Fcategory/<slug:val>' ,views.FCategoryView.as_view(), name='Fcategory'),
    path('productD/<int:pk>' ,views.ProductDetail.as_view(), name='productD'),
    path('FproductD/<int:pk>' ,views.FProductDetail.as_view(), name='FproductD'),
    path('upload/', views.upload, name='upload'),

    #log in auth
    path('Registration/' ,views.RegistrationView.as_view(), name='Registration'),
    path('accounts/login/',auth_view.LoginView.as_view(template_name = 'app/login.html',authentication_form =LoginForm),name='login'),
    path('password_reset/',auth_view.PasswordResetView.as_view(template_name = 'app/password_reset.html',form_class=MyPasswordResetForm),name='password_reset'),
    path('changePassword/',auth_view.PasswordChangeView.as_view(template_name='app/changePassword.html'),name='changePassword'),
    path('logout/', auth_view.LogoutView.as_view(next_page='login'), name='logout'),
    #wishlist
    path('wishlist/', views.wishlist, name='wishlist'),
    path('add-to-wishlist/<int:product_id>/', views.add_to_wishlist, name='add_to_wishlist'),
    path('remove-from-wishlist/<int:product_id>/', views.remove_from_wishlist, name='remove_from_wishlist'),
    path('contact/success/', views.contact_success, name='contact_success'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
 