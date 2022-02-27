from django.views.generic import TemplateView, ListView, DetailView, DeleteView
from .models import Jockey, Venue, Stable, Mark, RaceInfo, RaceTable, RaceResults
from django.http import HttpResponse
from django.shortcuts import render
from django.db.models import Q
from django.urls import reverse_lazy
import datetime

# # Create your views here.

# ============『ホーム画面』=====================================================================================
class HomeView(ListView):
    model = RaceInfo
    queryset = RaceInfo.objects.all().select_related()
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)

        dt_today = datetime.datetime.now()
        dt_yesterday = dt_today - datetime.timedelta(days=1)
        dt_tomorrow = dt_today - datetime.timedelta(days=-1)
        today = dt_today.strftime('%Y/%m/%d') # 2022/##/##
        yesterday = dt_yesterday.strftime('%Y/%m/%d')
        tomorrow = dt_tomorrow.strftime('%Y/%m/%d')
        ctx['today'] = today
        ctx['yesterday'] = yesterday
        ctx['tomorrow'] = tomorrow
        ctx['join_date_today'] = dt_today.strftime('%Y%m%d') # 2022####
        ctx['join_date_yesterday'] = dt_yesterday.strftime('%Y%m%d')
        ctx['join_date_tomorrow'] = dt_tomorrow.strftime('%Y%m%d')

        ctx['today_races'] = RaceInfo.objects.filter(date=today)
        ctx['yesterday_races'] = RaceInfo.objects.filter(date=yesterday)
        ctx['tomorrow_races'] = RaceInfo.objects.filter(date=tomorrow)
        return ctx

class OtherView(ListView):
    model = RaceInfo
    template_name = 'other.html'

class EditView(ListView):
    model = RaceInfo
    template_name = 'edit.html'

# ============『最近のレース画面』=====================================================================================
class PickView(ListView):
    model = RaceResults
    queryset = RaceResults.objects.all().select_related()
    template_name = 'pick.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        dt_today = datetime.datetime.now()
        dt_yesterday = dt_today - datetime.timedelta(days=1)
        dt_tomorrow = dt_today - datetime.timedelta(days=-1)
        today = dt_today.strftime('%Y/%m/%d') # 2022/##/##
        yesterday = dt_yesterday.strftime('%Y/%m/%d')
        tomorrow = dt_tomorrow.strftime('%Y/%m/%d')
        comparative_today = dt_today.strftime('%Y%m%d')
        comparative_yesterday = dt_yesterday.strftime('%Y%m%d')
        comparative_tomorrow = dt_tomorrow.strftime('%Y%m%d')

        join_date_today = self.kwargs.get('join_date_today')
        join_date_yesterday = self.kwargs.get('join_date_yesterday')
        join_date_tomorrow = self.kwargs.get('join_date_tomorrow')
        today_venue = self.kwargs.get('today_venue')
        yesterday_venue = self.kwargs.get('yesterday_venue')
        tomorrow_venue = self.kwargs.get('tomorrow_venue')

        query_a = self.request.GET.get('query_a', default="")
        query_b = self.request.GET.get('query_b', default="")
        query_c = self.request.GET.get('query_c', default="")

        if join_date_today == comparative_today:
            today_venue_id = [venue.id for venue in Venue.objects.filter(name=today_venue)] # 当日一開催場所のIDを取得[i]
            today_race_info = [today_race.id for today_race in RaceInfo.objects.filter(date=today, venue__in=today_venue_id)] # 日、場所指定[i]
            today_race_table = [today_table.id for today_table in RaceTable.objects.filter(raceinfo__in=today_race_info)] # 一開催場所の全レース取得[i,i,i,...]
            # horse_names = RaceResults.objects.filter(racetable__in=today_race_table).values('horse_name')
            jockeys = [today_jockey.jockey for today_jockey in RaceResults.objects.filter(racetable__in=today_race_table).distinct()]
            jockeys = [today_jockey for today_jockey in Jockey.objects.filter(name__in=jockeys).values('name')]
            stables = [today_stable.stable for today_stable in RaceResults.objects.filter(racetable__in=today_race_table).distinct()]
            stables = [today_stable for today_stable in Stable.objects.filter(name__in=stables).values('name')]
            if query_a:
                race_results = RaceResults.objects.filter(racetable__in=today_race_table).filter(Q(horse_name__icontains=query_a))
            elif query_b:
                Jockey_id = [Jockey_id.id for Jockey_id in Jockey.objects.filter(name=query_b)]
                race_results = RaceResults.objects.filter(racetable__in=today_race_table).filter(Q(jockey__in=Jockey_id))
            elif query_c:
                stable_id = [stable_id.id for stable_id in Stable.objects.filter(name=query_c)]
                race_results = RaceResults.objects.filter(racetable__in=today_race_table).filter(Q(stable__in=stable_id))
            else:
                race_results = RaceResults.objects.filter(racetable__in=today_race_table)
        elif join_date_yesterday == comparative_yesterday:
            yesterday_venue_id = [venue.id for venue in Venue.objects.filter(name=yesterday_venue)]
            yesterday_race_info = [yesterday_race.id for yesterday_race in RaceInfo.objects.filter(date=yesterday, venue__in=yesterday_venue_id)]
            yesterday_race_table = [yesterday_table.id for yesterday_table in RaceTable.objects.filter(raceinfo__in=yesterday_race_info)]
            jockeys = [yesterday_jockey.jockey for yesterday_jockey in RaceResults.objects.filter(racetable__in=yesterday_race_table).distinct()]
            jockeys = [yesterday_jockey for yesterday_jockey in Jockey.objects.filter(name__in=jockeys).values('name')]
            stables = [yesterday_stable.stable for yesterday_stable in RaceResults.objects.filter(racetable__in=yesterday_race_table).distinct()]
            stables = [yesterday_stable for yesterday_stable in Stable.objects.filter(name__in=stables).values('name')]
            if query_a:
                race_results = RaceResults.objects.filter(racetable__in=yesterday_race_table).filter(Q(horse_name__icontains=query_a))
            elif query_b:
                Jockey_id = [Jockey_id.id for Jockey_id in Jockey.objects.filter(name=query_b)]
                race_results = RaceResults.objects.filter(racetable__in=yesterday_race_table).filter(Q(jockey__in=Jockey_id))
            elif query_c:
                stable_id = [stable_id.id for stable_id in Stable.objects.filter(name=query_c)]
                race_results = RaceResults.objects.filter(racetable__in=yesterday_race_table).filter(Q(stable__in=stable_id))
            else:
                race_results = RaceResults.objects.filter(racetable__in=yesterday_race_table)
        elif join_date_tomorrow == comparative_tomorrow:
            tomorrow_venue_id = [venue.id for venue in Venue.objects.filter(name=tomorrow_venue)]
            tomorrow_race_info = [tomorrow_race.id for tomorrow_race in RaceInfo.objects.filter(date=tomorrow, venue__in=tomorrow_venue_id)]
            tomorrow_race_table = [tomorrow_table.id for tomorrow_table in RaceTable.objects.filter(raceinfo__in=tomorrow_race_info)]
            jockeys = [tomorrow_jockey.jockey for tomorrow_jockey in RaceResults.objects.filter(racetable__in=tomorrow_race_table).distinct()]
            jockeys = [tomorrow_jockey for tomorrow_jockey in Jockey.objects.filter(name__in=jockeys).values('name')]
            stables = [tomorrow_stable.stable for tomorrow_stable in RaceResults.objects.filter(racetable__in=tomorrow_race_table).distinct()]
            stables = [tomorrow_stable for tomorrow_stable in Stable.objects.filter(name__in=stables).values('name')]
            if query_a:
                race_results = RaceResults.objects.filter(racetable__in=tomorrow_race_table).filter(Q(horse_name__icontains=query_a))
            elif query_b:
                Jockey_id = [Jockey_id.id for Jockey_id in Jockey.objects.filter(name=query_b)]
                race_results = RaceResults.objects.filter(racetable__in=tomorrow_race_table).filter(Q(jockey__in=Jockey_id))
            elif query_c:
                stable_id = [stable_id.id for stable_id in Stable.objects.filter(name=query_c)]
                race_results = RaceResults.objects.filter(racetable__in=tomorrow_race_table).filter(Q(stable__in=stable_id))
            else:
                race_results = RaceResults.objects.filter(racetable__in=tomorrow_race_table)
        else:
            print('else')
            race_results = None

        ctx['jockeys'] = jockeys
        ctx['stables'] = stables
        ctx['race_results'] = race_results
        return ctx

# ============『開催日で探す』に関するVIEW=====================================================================================
class DateSearchView(ListView): # 日付選択画面
    model = RaceInfo
    template_name = 'd_search.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        return ctx

class DateNextView(ListView): # 開催場所選択画面
    model = RaceInfo
    template_name = 'd_next.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)

        query_date = self.request.GET.get('query_date', default="")
        join_date = query_date.replace('-', '')
        search_venues = None
        if join_date:
            search_date = datetime.datetime.strptime(join_date, '%Y%m%d')
            search_date = search_date.strftime('%Y/%m/%d')
            search_venues = [search_venues.venue_id for search_venues in RaceInfo.objects.filter(date=search_date)]
            search_venues = [search_venues for search_venues in Venue.objects.filter(id__in=search_venues)]

        ctx['search_date'] = search_date
        ctx['join_date'] = join_date
        ctx['search_venues'] = search_venues
        return ctx

class DateResultView(ListView): # 検索レース表示画面
    model = RaceInfo
    template_name = 'd_result.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)

        query_date = self.request.GET.get('query_date', default="")
        query_venue = self.request.GET.get('query_venue', default="")
        ctx['query_date'] = query_date
        ctx['query_venue'] = query_venue

        query_a = self.request.GET.get('query_a', default="")
        query_b = self.request.GET.get('query_b', default="")
        query_c = self.request.GET.get('query_c', default="")

        jockeys = None
        stables = None
        search_results = None
        if query_date and query_venue:
            search_date = datetime.datetime.strptime(query_date, '%Y%m%d')
            search_date = search_date.strftime('%Y/%m/%d')
            search_venue_id = [venue.id for venue in Venue.objects.filter(name=query_venue)]
            search_race_info = [search_race.id for search_race in RaceInfo.objects.filter(date=search_date, venue__in=search_venue_id)]
            search_race_table = [search_table.id for search_table in RaceTable.objects.filter(raceinfo__in=search_race_info)]
            search_results = RaceResults.objects.filter(racetable__in=search_race_table)

            jockeys = [today_jockey.jockey for today_jockey in RaceResults.objects.filter(racetable__in=search_race_table).distinct()]
            jockeys = [today_jockey for today_jockey in Jockey.objects.filter(name__in=jockeys).values('name')]
            stables = [today_stable.stable for today_stable in RaceResults.objects.filter(racetable__in=search_race_table).distinct()]
            stables = [today_stable for today_stable in Stable.objects.filter(name__in=stables).values('name')]

            if query_a:
                search_results = RaceResults.objects.filter(racetable__in=search_race_table).filter(Q(horse_name__icontains=query_a))
            elif query_b:
                Jockey_id = [Jockey_id.id for Jockey_id in Jockey.objects.filter(name=query_b)]
                search_results = RaceResults.objects.filter(racetable__in=search_race_table).filter(Q(jockey__in=Jockey_id))
            elif query_c:
                stable_id = [stable_id.id for stable_id in Stable.objects.filter(name=query_c)]
                search_results = RaceResults.objects.filter(racetable__in=search_race_table).filter(Q(stable__in=stable_id))

        ctx['jockeys'] = jockeys
        ctx['stables'] = stables
        ctx['search_results'] = search_results
        return ctx


# ============『開催場所で探す』関連のVIEW=====================================================================================
class VenueSearchView(ListView):
    model = RaceInfo
    template_name = 'v_search.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        venues =  Venue.objects.all()
        ctx['venues'] = venues
        return ctx

class VenueNextView(ListView):
    model = RaceInfo
    template_name = 'v_next.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)

        query_venue = self.request.GET.get('query_venue', default="")
        search_venue_id = [search_venue.id for search_venue in Venue.objects.filter(name=query_venue)]
        search_dates = [search_date.date for search_date in RaceInfo.objects.filter(venue__in=search_venue_id)]

        date_list = [search_date for search_date in search_dates] # 2022##/##形式のリスト
        join_date_list = [] # 2022####形式のリスト
        for date in date_list: # ['2022/02/06', '2022/02/08', '2022/02/12', '2022/02/13']
            date = datetime.datetime.strptime(date, '%Y/%m/%d')
            join_date = date.strftime('%Y%m%d') # ['20220206', '20220208', '20220212', '20220213']
            join_date_list.append(join_date)
        search_dates_dict = {k: v for k, v in zip(date_list, join_date_list)}
        print('search_dates_dict', search_dates_dict, type(search_dates_dict))

        ctx['query_venue'] = query_venue
        ctx['search_dates_dict'] = search_dates_dict
        return ctx

class VenueResultView(ListView):
    model = RaceInfo
    template_name = 'v_result.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)

        query_date = self.request.GET.get('query_date', default="")
        query_venue = self.request.GET.get('query_venue', default="")
        ctx['query_date'] = query_date
        ctx['query_venue'] = query_venue

        query_a = self.request.GET.get('query_a', default="")
        query_b = self.request.GET.get('query_b', default="")
        query_c = self.request.GET.get('query_c', default="")

        search_results = None
        if query_date and query_venue:
            search_date = datetime.datetime.strptime(query_date, '%Y%m%d')
            search_date = search_date.strftime('%Y/%m/%d')
            search_venue_id = [venue.id for venue in Venue.objects.filter(name=query_venue)]
            search_race_info = [search_race.id for search_race in RaceInfo.objects.filter(date=search_date, venue__in=search_venue_id)]
            search_race_table = [search_table.id for search_table in RaceTable.objects.filter(raceinfo__in=search_race_info)]
            search_results = RaceResults.objects.filter(racetable__in=search_race_table)

            jockeys = [today_jockey.jockey for today_jockey in RaceResults.objects.filter(racetable__in=search_race_table).distinct()]
            jockeys = [today_jockey for today_jockey in Jockey.objects.filter(name__in=jockeys).values('name')]
            stables = [today_stable.stable for today_stable in RaceResults.objects.filter(racetable__in=search_race_table).distinct()]
            stables = [today_stable for today_stable in Stable.objects.filter(name__in=stables).values('name')]

            if query_a:
                search_results = RaceResults.objects.filter(racetable__in=search_race_table).filter(Q(horse_name__icontains=query_a))
            elif query_b:
                Jockey_id = [Jockey_id.id for Jockey_id in Jockey.objects.filter(name=query_b)]
                search_results = RaceResults.objects.filter(racetable__in=search_race_table).filter(Q(jockey__in=Jockey_id))
            elif query_c:
                stable_id = [stable_id.id for stable_id in Stable.objects.filter(name=query_c)]
                search_results = RaceResults.objects.filter(racetable__in=search_race_table).filter(Q(stable__in=stable_id))

        ctx['jockeys'] = jockeys
        ctx['stables'] = stables
        ctx['search_results'] = search_results
        return ctx


# ============『レース整理』関連のVIEW=====================================================================================
class OrganizeView(ListView):
    model = RaceInfo
    template_name = 'organize.html'
    paginate_by = 20

class DetailView(DetailView):
    model = RaceInfo
    template_name = 'detail.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)

        query_pk = self.request.GET.get('pk', default="")
        race_info = RaceInfo.objects.filter(pk=query_pk)
        race_table = RaceTable.objects.filter(raceinfo__in=race_info)
        race_results = RaceResults.objects.filter(racetable__in=race_table)
        ctx['race_results'] = race_results
        return ctx

class DeleteView(DeleteView):
    model = RaceInfo
    template_name = 'delete.html'
    success_url = reverse_lazy('organize')


def making(request):
    return render(request, 'making.html')

def use(request):
    return render(request, 'use.html')


# ####################################################################################################

# def sample(request):
#     print("sample")
#     date = datetime.datetime.strptime(join_date, '%Y%m%d')
#     date = date.strftime('%Y/%m/%d')
#     venues = RaceInfo.objects.filter(date=date).values('venue').distinct()
#     venues = { 'venues': venues }
#     return render(request, 'therace.html', venues)

# def dispatch(self, request, *args, **kwargs,):
#     print('DISPATCH')
#     return super().dispatch(request, *args, **kwargs)

# def get(self, request, *args, **kwargs):
#     print('GET')
#     return super().get(request, *args, **kwargs)

# def post(self, request, *args, **kwargs):
#     print('POST')
#     return HttpResponse(200)