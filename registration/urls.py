from django.urls import path
from .views import SignUpView, ActivateAccount, ProfileView, AddcustomerView, CustomerView, deleteaddress
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('profile/<int:pk>/', ProfileView.as_view(), name='profile'),
    path('activate/<uidb64>/<token>/', ActivateAccount.as_view(), name='activate'),
    path('login/', auth_views.LoginView.as_view(redirect_authenticated_user=True, template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    #Customers
    path('addcustomer/', AddcustomerView.as_view(), name='addcustomer'),
    path('customers/', CustomerView.as_view(), name='customers'),
    path('deleteaddress/<int:id>/', deleteaddress, name='deleteaddress'),
    # Change Password
    path('change-password/',auth_views.PasswordChangeView.as_view(template_name='registration/change-password.html',success_url = '/'),name='change_password'),
    # Forget Password
    path('password-reset/',auth_views.PasswordResetView.as_view(template_name='registration/password-reset/password_reset.html',subject_template_name='registration/password-reset/password_reset_subject.txt',email_template_name='registration/password-reset/password_reset_email.html',success_url='/password-reset/done/'),name='password_reset'),
    path('password-reset/done/',auth_views.PasswordResetDoneView.as_view(template_name='registration/password-reset/password_reset_done.html'),name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name='registration/password-reset/password_reset_confirm.html'),name='password_reset_confirm'),
    path('password-reset-complete/',auth_views.PasswordResetCompleteView.as_view(template_name='registration/password-reset/password_reset_complete.html'),name='password_reset_complete'),
]