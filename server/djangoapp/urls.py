from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views

app_name = 'djangoapp'
urlpatterns = [
    # route is a string contains a URL pattern
    # view refers to the view function
    # name the URL

    path(route='', view=views.get_dealerships, name='index'),

    path(route='about/', view=views.get_about_us, name='about'),

    path(route='contact_us/', view=views.get_contact_us, name='contact_us'),

    path(route='registration/', view=views.registration_request, name='registration'),

    path(route='login/', view=views.login_request, name='login'),

    path(route='logout/', view=views.logout_request, name='logout'),

    # path for dealer reviews view

    # path for add a review view

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)