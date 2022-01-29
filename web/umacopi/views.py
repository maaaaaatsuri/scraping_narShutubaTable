from django.views.generic import TemplateView, ListView, DetailView, DeleteView
from .models import NarModel
from django.http import HttpResponse
from django.shortcuts import render
from django.db.models import Q
import datetime

# Create your views here.

class HomeView(ListView):
    model = NarModel
    queryset = NarModel.objects.values('held_date','venue').distinct()
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
        ctx['today_con'] = dt_today.strftime('%Y%m%d') # 2022####
        ctx['yesterday_con'] = dt_yesterday.strftime('%Y%m%d')
        ctx['tomorrow_con'] = dt_tomorrow.strftime('%Y%m%d')

        ctx['todayraces'] = NarModel.objects.all()
        ctx['todayraces'] = NarModel.objects.filter(held_date=today).values('held_date','venue').distinct()
        ctx['yesterdayraces'] = NarModel.objects.filter(held_date=yesterday).values('held_date','venue').distinct()
        ctx['tomorrowraces'] = NarModel.objects.filter(held_date=tomorrow).values('held_date','venue').distinct()
        
        held_dates = NarModel.objects.values('held_date').distinct().order_by('held_date')
        date_list = [] # 2022##/##形式のリスト
        join_date_list = [] # 2022####形式のリスト
        for held_date in held_dates:
            for date in held_date.values():
                date_list.append(date)
                date = datetime.datetime.strptime(date, '%Y/%m/%d')
                join_date = date.strftime('%Y%m%d')
                join_date_list.append(join_date)
        datedict = {k: v for k, v in zip(date_list, join_date_list)}
        ctx['datedict'] = datedict
        ctx['venues'] = NarModel.objects.values('venue').distinct()
        
        query_date = self.request.GET.get('query_date', default="")
        if query_date:
            date = datetime.datetime.strptime(query_date, '%Y%m%d')
            date = date.strftime('%Y/%m/%d')
            filtering_venues = NarModel.objects.filter(held_date=date).values('held_date', 'venue').distinct()
            ctx['filtering_venues'] = filtering_venues
        else:
            pass
        
        return ctx


class PickView(ListView):
    model = NarModel
    template_name = 'pick.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        dt_today = datetime.datetime.now()
        dt_yesterday = dt_today - datetime.timedelta(days=1)
        dt_tomorrow = dt_today - datetime.timedelta(days=-1)

        today = dt_today.strftime('%Y/%m/%d') # 2022/##/##
        yesterday = dt_yesterday.strftime('%Y/%m/%d')
        tomorrow = dt_tomorrow.strftime('%Y/%m/%d')
        
        tod = dt_today.strftime('%Y%m%d')
        ye = dt_yesterday.strftime('%Y%m%d')
        tom = dt_tomorrow.strftime('%Y%m%d')
        
        today_con = self.kwargs.get('today_con')
        today_venue = self.kwargs.get('today_venue')
        yesterday_con = self.kwargs.get('yesterday_con')
        yesterday_venue = self.kwargs.get('yesterday_venue')
        tomorrow_con = self.kwargs.get('tomorrow_con')
        tomorrow_venue = self.kwargs.get('tomorrow_venue')

        query_a = self.request.GET.get('query_a', default="")
        query_b = self.request.GET.get('query_b', default="")
        query_c = self.request.GET.get('query_c', default="")

        if today_con == tod:
            horsenames = NarModel.objects.filter(held_date=today, venue=today_venue).values('horse_name')
            jockeys = NarModel.objects.filter(held_date=today, venue=today_venue).values('jockey').distinct()
            stables = NarModel.objects.filter(held_date=today, venue=today_venue).values('stable').distinct()
            if query_a:
                pickdata = NarModel.objects.filter(held_date=today, venue=today_venue).values().filter(Q(horse_name__icontains=query_a))
            elif query_b:
                pickdata = NarModel.objects.filter(held_date=today, venue=today_venue).values().filter(Q(jockey__iexact=query_b)).distinct()
            elif query_c:
                pickdata = NarModel.objects.filter(held_date=today, venue=today_venue).values().filter(Q(stable__iexact=query_c)).distinct()
            else:
                pickdata = NarModel.objects.filter(held_date=today, venue=today_venue).values()
        elif yesterday_con == ye:
            horsenames = NarModel.objects.filter(held_date=yesterday, venue=yesterday_venue).values('horse_name')
            jockeys = NarModel.objects.filter(held_date=yesterday, venue=yesterday_venue).values('jockey').distinct()
            stables = NarModel.objects.filter(held_date=yesterday, venue=yesterday_venue).values('stable').distinct()
            if query_a:
                pickdata = NarModel.objects.filter(held_date=yesterday, venue=yesterday_venue).values().filter(Q(horse_name__icontains=query_a)).distinct()
            elif query_b:
                pickdata = NarModel.objects.filter(held_date=yesterday, venue=yesterday_venue).values().filter(Q(jockey__iexact=query_b)).distinct()
            elif query_c:
                pickdata = NarModel.objects.filter(held_date=yesterday, venue=yesterday_venue).values().filter(Q(stable__iexact=query_c)).distinct()
            else:
                pickdata = NarModel.objects.filter(held_date=yesterday, venue=yesterday_venue).values()
        elif tomorrow_con == tom:
            horsenames = NarModel.objects.filter(held_date=tomorrow, venue=tomorrow_venue).values('horse_name')
            jockeys = NarModel.objects.filter(held_date=tomorrow, venue=tomorrow_venue).values('jockey').distinct()
            stables = NarModel.objects.filter(held_date=tomorrow, venue=tomorrow_venue).values('stable').distinct()
            if query_a:
                pickdata = NarModel.objects.filter(held_date=tomorrow, venue=tomorrow_venue).values().filter(Q(horse_name__icontains=query_a)).distinct()
            elif query_b:
                pickdata = NarModel.objects.filter(held_date=tomorrow, venue=tomorrow_venue).values().filter(Q(jockey__iexact=query_b)).distinct()
            elif query_c:
                pickdata = NarModel.objects.filter(held_date=tomorrow, venue=tomorrow_venue).values().filter(Q(stable__iexact=query_c)).distinct()
            else:
                pickdata = NarModel.objects.filter(held_date=tomorrow, venue=tomorrow_venue).values()
        else:
            pickdata = NarModel.objects.all()
        ctx['horsenames'] = horsenames
        ctx['jockeys'] = jockeys
        ctx['stables'] = stables
        ctx['pickdata'] = pickdata
        return ctx


class DateSearchView(ListView):
    model = NarModel
    template_name = 'date.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)

        held_dates = NarModel.objects.values('held_date').distinct().order_by('held_date')
        date_list = [] # 2022##/##形式のリスト
        join_date_list = [] # 2022####形式のリスト
        for held_date in held_dates:
            for date in held_date.values():
                date_list.append(date)
                date = datetime.datetime.strptime(date, '%Y/%m/%d')
                join_date = date.strftime('%Y%m%d')
                join_date_list.append(join_date)
        datedict = {k: v for k, v in zip(date_list, join_date_list)}
        ctx['datedict'] = datedict

        dateselected = NarModel.objects.none()
        filtering_venues = NarModel.objects.none()
        query_date = self.request.GET.get('query_date', default="")
        if query_date:
            date = datetime.datetime.strptime(query_date, '%Y%m%d')
            date = date.strftime('%Y/%m/%d')
            filtering_venues = NarModel.objects.filter(held_date=date).values('venue').distinct()
            dateselected = NarModel.objects.filter(held_date=date).values()
        else:
            pass
        
        query_venue = self.request.GET.get('query_venue', default="")
        if query_venue:
            dateselected = NarModel.objects.filter(held_date=date, venue=query_venue).values()
        else:
            pass

        ctx['filtering_venues'] = filtering_venues
        ctx['dateselected'] = dateselected
        return ctx


class VenueSelectedView(ListView):
    model = NarModel
    template_name = 'a.html'

    # def get_context_data(self, **kwargs):
    #     ctx = super().get_context_data(**kwargs)

    #     selected_venue = self.kwargs.get('selected_venue')
    #     date = NarModel.objects.filter(venue=selected_venue).values('held_date').distinct()

    #     join_date = self.request.GET.get('join_date', default="")
    #     a = datetime.datetime.strptime(join_date, '%Y%m%d')
    #     a = a.strftime('%Y/%m/%d')
    #     b = NarModel.objects.none()

    #     if join_date:
    #         b = NarModel.objects.filter(held_date=a, venue=selected_venue).values()
    #     else:
    #         pass

    #     ctx['date'] = date
    #     ctx['b'] = b
    #     return ctx


class aView(ListView):
    model = NarModel
    template_name = 'datesearch.html'

#     def get_context_data(self, **kwargs):
#         ctx = super().get_context_data(**kwargs)
#         held_dates = NarModel.objects.values('held_date').distinct().order_by('held_date')
#         held_venues = NarModel.objects.values('venue').distinct()

#         date_list = [] # 2022##/##形式のリスト
#         join_date_list = [] # 2022####形式のリスト
#         for held_date in held_dates:
#             for date in held_date.values():
#                 date_list.append(date)
#                 date = datetime.datetime.strptime(date, '%Y/%m/%d')
#                 join_date = date.strftime('%Y%m%d')
#                 join_date_list.append(join_date)
#         datedict = {k: v for k, v in zip(date_list, join_date_list)}
#         ctx['datedict'] = datedict
#         ctx['held_venues'] = held_venues
#         return ctx


# <h5>◆開催場所から探す</h5>
# <label for="select_venue">開催日を選択してください:</label><br>
#   {% for v in venues %}
#     <a href='{% url "v_search" %}'>{{ v.venue }}</a>
#   {% endfor %}








####################################################################################################


# def sample(request):
#     print("sample")
#     date = datetime.datetime.strptime(join_date, '%Y%m%d')
#     date = date.strftime('%Y/%m/%d')
#     venues = NarModel.objects.filter(held_date=date).values('venue').distinct()
#     venues = { 'venues': venues }
#     return render(request, 'therace.html', venues)


        # join_date = self.kwargs.get('join_date')
    
        # if join_date:
        #     date = datetime.datetime.strptime(join_date, '%Y%m%d')
        #     date = date.strftime('%Y/%m/%d')
        #     venues = NarModel.objects.filter(held_date=date).values('venue').distinct()
        # else:
        #     print("else")
        #     pass





class VenueSearchView(ListView):
    model = NarModel
    template_name = 'search.html'

    # def get_context_data(self, **kwargs):
    #     ctx = super().get_context_data(**kwargs)

    #     pickdatav = NarModel.objects.values('venue').distinct()
    #     ctx['pickdatav'] = pickdatav
    #     return ctx





        # join_date = self.kwargs.get('join_date')
        # # query_c = self.request.GET.get('query_c', default="")
        # print(join_date)

        # if join_date:
        #     date_search_venue = NarModel.objects.filter(held_date=join_date).values('venue')
        # #     if query_a:
        # #         pickdata = NarModel.objects.filter(held_date=today, venue=today_venue).values().filter(Q(horse_name__icontains=query_a))
        # #     elif query_b:
        # #         pickdata = NarModel.objects.filter(held_date=today, venue=today_venue).values().filter(Q(jockey__iexact=query_b)).distinct()
        # #     elif query_c:
        # #         pickdata = NarModel.objects.filter(held_date=today, venue=today_venue).values().filter(Q(stable__iexact=query_c)).distinct()
        # #     else:
        # #         pickdata = NarModel.objects.filter(held_date=today, venue=today_venue).values()
        # # elif yesterday_con == ye:
        # else:
        #     pass

        # # ctx['datesearchvenue'] = date_search_venue





















# def dispatch(self, request, *args, **kwargs,):
#     print('DISPATCH')
#     return super().dispatch(request, *args, **kwargs)

# def get(self, request, *args, **kwargs):
#     print('GET')
#     return super().get(request, *args, **kwargs)

# def post(self, request, *args, **kwargs):
#     print('POST')
#     return HttpResponse(200)



# def today_pick(request, today_con, today_venue):
#     dt_today = datetime.datetime.now()
#     today = dt_today.strftime('%Y/%m/%d')
#     pickdata = NarModel.objects.filter(held_date=today, venue=today_venue).values()
#     ctx = { 'pickdata': pickdata,
#             'today': today,
#             'today_con': today_con}
#     return render(request, 'pick.html', ctx)

# def yesterday_pick(request, yesterday_con, yesterday_venue):
#     dt_today = datetime.datetime.now()
#     dt_yesterday = dt_today - datetime.timedelta(days=1)
#     yesterday = dt_yesterday.strftime('%Y/%m/%d')
#     pickdata = NarModel.objects.filter(held_date=yesterday, venue=yesterday_venue).values()
#     ctx = { 'pickdata': pickdata,
#             'yesterday': yesterday,
#             'yesterday_con': yesterday_con}
#     return render(request, 'pick.html', ctx)

# def tomorrow_pick(request, tomorrow_con, tomorrow_venue):
#     dt_today = datetime.datetime.now()
#     dt_tomorrow = dt_today - datetime.timedelta(days=-1)
#     tomorrow = dt_tomorrow.strftime('%Y/%m/%d')
#     pickdata = NarModel.objects.filter(held_date=tomorrow, venue=tomorrow_venue).values()
#     ctx = { 'pickdata': pickdata,
#             'tomorrow': tomorrow,
#             'tomorrow_con': tomorrow_con}
#     return render(request, 'pick.html', ctx)



# class DeleteView(DeleteView):
#     model = NarModel
#     template_name = 'delete.html'
#     success_url = reverse_lazy('pick')

        # ctx['today_venue'] = NarModel.objects.filter(held_date=today).values('venue').distinct()
        # ctx['yesterday_venue'] = NarModel.objects.filter(held_date=yesterday).values('venue').distinct()
        # ctx['tomorrow_venue'] = NarModel.objects.filter(held_date=tomorrow).values('venue').distinct()