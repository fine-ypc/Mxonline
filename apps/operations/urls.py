from django.conf.urls import url
from django.urls import path
from apps.operations.views import UserFavView, CourseCommentsView
from django.views.decorators.csrf import csrf_exempt


urlpatterns = [
    url(r'^fav/$', UserFavView.as_view(), name="fav"),
    url(r'^comment/$', CourseCommentsView.as_view(), name="comment"),

]
