from django.conf.urls import url
from django.urls import path
from apps.organizations.views import OrgListView, UserAskView, OrgHomeView, OrgTeacherView, OrgCourseView, OrgDescView

urlpatterns = [
    url(r'^list/$', OrgListView.as_view(), name="list"),
    url(r'^add_ask/$', UserAskView.as_view(), name="add_ask"),
    path('<int:org_id>/', OrgHomeView.as_view(), name="home"),
    path('<int:org_id>/teacher/', OrgTeacherView.as_view(), name="teacher"),
    path('<int:org_id>/course/', OrgCourseView.as_view(), name="course"),
    path('<int:org_id>/desc/', OrgDescView.as_view(), name="desc"),
]
