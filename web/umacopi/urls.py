from django.urls import path
from . import views
# from .views import HomeView, PickView, DateSearchView, VenueSearchView
# from .views import aView, VenueSelectedView, DeleteView

"""
path(第1引数:webブラウザから呼出すURLの名称, 第2引数:呼び出される関数, 第3引数:htmlファイルからの呼び出しに使う)
(第3引数について、「"http://localhost:8000/アプリ名/第1引数"」を、第3引数「{% url 'name' %}」と記述することが可能。)
"""

urlpatterns = [
    # path('home/', HomeView.as_view(), name='home'),
    # path('today_pick/<str:today_con>/<str:today_venue>', PickView.as_view(), name='today_pick'),
    # path('yesterday_pick/<str:yesterday_con>/<str:yesterday_venue>', PickView.as_view(), name='yesterday_pick'),
    # path('tomorrow_pick/<str:tomorrow_con>/<str:tomorrow_venue>', PickView.as_view(), name='tomorrow_pick'),

    # path('home/d_search/', DateSearchView.as_view(), name='d_search'),

    # path('home/v_search', DateSearchView.as_view(), name='v_search'),



    # path('d_search/<str:join_date>', DateSelectedView.as_view(), name='da_search'),
    # path('d_search/<str:join_date>/<str:selected_venue>', DateSelectedView.as_view(), name='selected_venue'),    
    
    # path('v_search/', VenueSearchView.as_view(), name='v_search'),

    # path('search/<str:join_date>', DateSelectedView.as_view(), name='join_date'),
    

    # path('search/<str:selected_venue>', VenueSelectedView.as_view(), name='s'),
    # path('search/<str:selected_venue>/<str:join_date>', VenueSelectedView.as_view(), name='ss'),

    # # path('delete/', DeleteView.as_view(), name='delete'),
]