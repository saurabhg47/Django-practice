from django.conf.urls import include, url
from assignment_interviewer import views

urlpatterns = [
     url(r'^login/$', views.dashboard, name='dashboard'),
     url(r'^registeruserpage/$', views.register_user_page, name='User Registration'),
     url(r'^registeruser/$', views.register_user, name='User Registration'),
     url(r'^loginuser/$', views.login_user, name='Log In'),
     url(r'^addcandidate/$', views.add_candidate, name='Add Candidate'),
     url(r'^addnewcandidate/$', views.add_new_candidate, name='Add Candidate'),
     url(r'^gotoratecandidate/$', views.go_to_rate_candidate, name='Go To Rate Candidate Page'),
     url(r'^ratecandidate/$', views.rate_candidate, name='Rate Candidate'),
     url(r'^logout/$', views.logout_user, name='LogOut User'),
     url(r'^hrlogin/$', views.hr_login, name='Hr Login'),
]
