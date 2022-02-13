from django.urls import path
from . import views
from .views import HomeView, PickView, DateSearchView, DateNextView,  DateResultView
from .views import VenueSearchView, VenueNextView, VenueResultView
# from .views import aView, VenueSelectedView, DeleteView

"""
path(第1引数:webブラウザから呼出すURLの名称, 第2引数:呼び出される関数, 第3引数:htmlファイルからの呼び出しに使う)
(第3引数について、「"http://localhost:8000/アプリ名/第1引数"」を、第3引数「{% url 'name' %}」と記述することが可能。)
"""

urlpatterns = [
    path('home/', HomeView.as_view(), name='home'),
    path('yesterday/<str:join_date_yesterday>/<str:yesterday_venue>', PickView.as_view(), name='yesterday'),
    path('today/<str:join_date_today>/<str:today_venue>', PickView.as_view(), name='today'),
    path('tomorrow/<str:join_date_tomorrow>/<str:tomorrow_venue>', PickView.as_view(), name='tomorrow'),

    path('home/d_search/', DateSearchView.as_view(), name='d_search'),
    path('home/d_search/next', DateNextView.as_view(), name='d_search_next'),
    path('home/d_search/result', DateResultView.as_view(), name='d_search_result'),

    path('home/v_search', VenueSearchView.as_view(), name='v_search'),
    path('home/v_search/next', VenueNextView.as_view(), name='v_search_next'),
    path('home/v_search/result', VenueResultView.as_view(), name='v_search_result'),


    # path('v_search/', VenueSearchView.as_view(), name='v_search'),
    # path('search/<str:join_date>', DateSelectedView.as_view(), name='join_date'),
    # path('search/<str:selected_venue>', VenueSelectedView.as_view(), name='s'),
    # path('search/<str:selected_venue>/<str:join_date>', VenueSelectedView.as_view(), name='ss'),
    # # path('delete/', DeleteView.as_view(), name='delete'),
]