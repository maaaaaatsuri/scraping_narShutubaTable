from django.urls import path
from . import views
from .views import HomeView, OtherView, EditView, PickView
from .views import DateSearchView, DateNextView,  DateResultView
from .views import VenueSearchView, VenueNextView, VenueResultView
from .views import OrganizeView, DetailView, DeleteView


urlpatterns = [
    path("making/", views.making, name="making"),
    path("use/", views.use, name="use"),

    path('home/', HomeView.as_view(), name='home'),
    path('other/', OtherView.as_view(), name='other'),
    path('edit/', EditView.as_view(), name='edit'),

    path('yesterday/<str:join_date_yesterday>/<str:yesterday_venue>', PickView.as_view(), name='yesterday'),
    path('today/<str:join_date_today>/<str:today_venue>', PickView.as_view(), name='today'),
    path('tomorrow/<str:join_date_tomorrow>/<str:tomorrow_venue>', PickView.as_view(), name='tomorrow'),

    path('home/d_search/', DateSearchView.as_view(), name='d_search'),
    path('home/d_search/next/', DateNextView.as_view(), name='d_search_next'),
    path('home/d_search/result/', DateResultView.as_view(), name='d_search_result'),

    path('home/v_search/', VenueSearchView.as_view(), name='v_search'),
    path('home/v_search/next/', VenueNextView.as_view(), name='v_search_next'),
    path('home/v_search/result/', VenueResultView.as_view(), name='v_search_result'),

    path('home/organize/', OrganizeView.as_view(), name='organize'),
    path('home/detail/<int:pk>/', DetailView.as_view(), name='detail_pk'),
    path('home/delete/<int:pk>/', DeleteView.as_view(), name='delete_pk'),
]