"""
URL configuration for Score_Sense project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from webapp.views import home
from webapp import views as webapp_views
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name="home"),  # Home page route
    path('signup/', webapp_views.signup_view, name='signup'),  # Signup page
    path('login/', webapp_views.login_view, name='login'),  # Login page
    path('credit_form/', webapp_views.credit_form, name='credit_form'),  # credit form page
    path('about_us/', webapp_views.about_us, name='about_us'),  # About us page
    path('contact/', webapp_views.contact, name='contact'),  # Contact page
    path('help/', webapp_views.help, name='help'),  # Help page
    path('tc/', webapp_views.tc, name='tc'),  # Terms and COnditions page
    path('tariff/', webapp_views.tariff, name='tariff'),  # tariff page
    path('dashboard/', webapp_views.dashboard, name='dashboard'),  # user_dashboard page
    path('user_home/', webapp_views.user_home, name='user_home'),  # user_home page
    path('loan_information/', webapp_views.loan_information, name='loan_information'),  # loan information page
    path('logout/', LogoutView.as_view(), name='logout'),
    path('credit_form/', webapp_views.credit_form, name='credit_form'),
    path('feedback/', webapp_views.feedback_form, name='feedback_form'),
    path('thank-you/', webapp_views.thank_you, name='thank_you'),
    path('financial_news/', webapp_views.fetch_financial_news, name='financial_news'),


]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])
