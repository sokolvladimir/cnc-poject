from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.urls import reverse_lazy


app_name = 'cncapp'


urlpatterns = [
    # Программа
    path('', views.create_cnc, name='create_cnc'),
    # login logout
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('password_reset/', auth_views.PasswordResetView.as_view(
        success_url=reverse_lazy('cncapp:password_reset_done')
    ), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
            success_url=reverse_lazy('cncapp:password_reset_complete')
    ), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('profile/', views.view_profile, name='profile'),
    path('register/', views.register, name='register'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    # Как программа работает
    path('how_it_made/', views.how_it_made, name='how_it_made'),
    # Запись индивидуальных значений пользователем
    path('my_cutters/', views.my_cutter, name='my_cutter'),
    # Категории
    path('category/', views.show_category, name='show_category'),
    path('category/<slug:slug>/', views.category_details, name='category_details'),
    # Статьи
    path('article/<int:y>/<int:m>/<int:d>/<slug:slug>/', views.information_details,
         name='information_details'),

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
