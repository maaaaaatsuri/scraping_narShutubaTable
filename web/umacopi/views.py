from django.views.generic import TemplateView, ListView, DetailView, DeleteView
from .models import NarModel
from django.http import HttpResponse
from django.shortcuts import render
from django.db.models import Q
import datetime

# Create your views here.

class HomeView(ListView):
    model = NarModel
    queryset = NarModel.objects.values('開催日','開催場所').distinct()
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

        ctx['todayraces'] = NarModel.objects.filter(開催日=today).values('開催日','開催場所').distinct()
        ctx['yesterdayraces'] = NarModel.objects.filter(開催日=yesterday).values('開催日','開催場所').distinct()
        ctx['tomorrowraces'] = NarModel.objects.filter(開催日=tomorrow).values('開催日','開催場所').distinct()
        
        ctx['thedates'] = NarModel.objects.values('開催日').distinct()
        ctx['thevenues'] = NarModel.objects.values('開催場所').distinct()
        return ctx


class PickView(ListView):
    model = NarModel
    template_name = 'pick.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
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
            horsenames = NarModel.objects.filter(開催日=today, 開催場所=today_venue).values('馬名')
            jockeys = NarModel.objects.filter(開催日=today, 開催場所=today_venue).values('騎手').distinct()
            stables = NarModel.objects.filter(開催日=today, 開催場所=today_venue).values('厩舎').distinct()
            if query_a:
                pickdata = NarModel.objects.filter(開催日=today, 開催場所=today_venue).values().filter(Q(馬名__icontains=query_a))
            elif query_b:
                pickdata = NarModel.objects.filter(開催日=today, 開催場所=today_venue).values().filter(Q(騎手__iexact=query_b)).distinct()
            elif query_c:
                pickdata = NarModel.objects.filter(開催日=today, 開催場所=today_venue).values().filter(Q(厩舎__iexact=query_c)).distinct()
            else:
                pickdata = NarModel.objects.filter(開催日=today, 開催場所=today_venue).values()
        elif yesterday_con == ye:
            horsenames = NarModel.objects.filter(開催日=yesterday, 開催場所=yesterday_venue).values('馬名')
            jockeys = NarModel.objects.filter(開催日=yesterday, 開催場所=yesterday_venue).values('騎手').distinct()
            stables = NarModel.objects.filter(開催日=yesterday, 開催場所=yesterday_venue).values('厩舎').distinct()
            if query_a:
                pickdata = NarModel.objects.filter(開催日=yesterday, 開催場所=yesterday_venue).values().filter(Q(馬名__icontains=query_a)).distinct()
            elif query_b:
                pickdata = NarModel.objects.filter(開催日=yesterday, 開催場所=yesterday_venue).values().filter(Q(騎手__iexact=query_b)).distinct()
            elif query_c:
                pickdata = NarModel.objects.filter(開催日=yesterday, 開催場所=yesterday_venue).values().filter(Q(厩舎__iexact=query_c)).distinct()
            else:
                pickdata = NarModel.objects.filter(開催日=yesterday, 開催場所=yesterday_venue).values()
        elif tomorrow_con == tom:
            horsenames = NarModel.objects.filter(開催日=tomorrow, 開催場所=tomorrow_venue).values('馬名')
            jockeys = NarModel.objects.filter(開催日=tomorrow, 開催場所=tomorrow_venue).values('騎手').distinct()
            stables = NarModel.objects.filter(開催日=tomorrow, 開催場所=tomorrow_venue).values('厩舎').distinct()
            if query_a:
                pickdata = NarModel.objects.filter(開催日=tomorrow, 開催場所=tomorrow_venue).values().filter(Q(馬名__icontains=query_a)).distinct()
            elif query_b:
                pickdata = NarModel.objects.filter(開催日=tomorrow, 開催場所=tomorrow_venue).values().filter(Q(騎手__iexact=query_b)).distinct()
            elif query_c:
                pickdata = NarModel.objects.filter(開催日=tomorrow, 開催場所=tomorrow_venue).values().filter(Q(厩舎__iexact=query_c)).distinct()
            else:
                pickdata = NarModel.objects.filter(開催日=tomorrow, 開催場所=tomorrow_venue).values()
        else:
            pickdata = NarModel.objects.all()
        context['horsenames'] = horsenames
        context['jockeys'] = jockeys
        context['stables'] = stables
        context['pickdata'] = pickdata
        return context


class DateSearchView(ListView):
    model = NarModel
    template_name = 'search.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        held_dates = NarModel.objects.values('開催日').distinct()
        held_venues = NarModel.objects.values('開催場所').distinct()

        date_list = [] # 2022##/##形式のリスト
        join_date_list = [] # 2022####形式のリスト
        for held_date in held_dates:
            for date in held_date.values():
                date_list.append(date)
                date = datetime.datetime.strptime(date, '%Y/%m/%d')
                join_date = date.strftime('%Y%m%d')
                join_date_list.append(join_date)
        datedict = {k: v for k, v in zip(date_list, join_date_list)}
        context['datedict'] = datedict
        context['held_venues'] = held_venues
        return context


class DateSelectedView(ListView):
    model = NarModel
    template_name = 'subsearch.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        join_date = self.kwargs.get('join_date')
        date = datetime.datetime.strptime(join_date, '%Y%m%d')
        date = date.strftime('%Y/%m/%d')

        venues = NarModel.objects.filter(開催日=date).values('開催場所').distinct()
        context['venues'] = venues
        
        a = NarModel.objects.all()
        selected_venue = self.request.GET.get('selected_venue', default="")
        if selected_venue:
            a = NarModel.objects.filter(開催日=date, 開催場所=selected_venue).values()
        else:
            print("elseのpass")
            a = NarModel.objects.filter(開催日=date).values()
            pass

        context['a'] = a
        return context

















####################################################################################################


# def sample(request):
#     print("sample")
#     date = datetime.datetime.strptime(join_date, '%Y%m%d')
#     date = date.strftime('%Y/%m/%d')
#     venues = NarModel.objects.filter(開催日=date).values('開催場所').distinct()
#     venues = { 'venues': venues }
#     return render(request, 'therace.html', venues)


        # join_date = self.kwargs.get('join_date')
    
        # if join_date:
        #     date = datetime.datetime.strptime(join_date, '%Y%m%d')
        #     date = date.strftime('%Y/%m/%d')
        #     venues = NarModel.objects.filter(開催日=date).values('開催場所').distinct()
        # else:
        #     print("else")
        #     pass





class VenueSearchView(ListView):
    model = NarModel
    template_name = 'search.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        pickdatav = NarModel.objects.values('開催場所').distinct()
        context['pickdatav'] = pickdatav
        return context





        # join_date = self.kwargs.get('join_date')
        # # query_c = self.request.GET.get('query_c', default="")
        # print(join_date)

        # if join_date:
        #     date_search_venue = NarModel.objects.filter(開催日=join_date).values('開催場所')
        # #     if query_a:
        # #         pickdata = NarModel.objects.filter(開催日=today, 開催場所=today_venue).values().filter(Q(馬名__icontains=query_a))
        # #     elif query_b:
        # #         pickdata = NarModel.objects.filter(開催日=today, 開催場所=today_venue).values().filter(Q(騎手__iexact=query_b)).distinct()
        # #     elif query_c:
        # #         pickdata = NarModel.objects.filter(開催日=today, 開催場所=today_venue).values().filter(Q(厩舎__iexact=query_c)).distinct()
        # #     else:
        # #         pickdata = NarModel.objects.filter(開催日=today, 開催場所=today_venue).values()
        # # elif yesterday_con == ye:
        # else:
        #     pass

        # # context['datesearchvenue'] = date_search_venue





















    # def dispatch(self, request, *args, **kwargs,):
    #     print('DISPATCH')
    #     return super().dispatch(request, *args, **kwargs)

    # def get(self, request, *args, **kwargs):
    #     print('GET')
    #     return super().get(request, *args, **kwargs)

    # def post(self, request, *args, **kwargs):
    #     print('POST')
    #     return HttpResponse(200)



def today_pick(request, today_con, today_venue):
    dt_today = datetime.datetime.now()
    today = dt_today.strftime('%Y/%m/%d')
    pickdata = NarModel.objects.filter(開催日=today, 開催場所=today_venue).values()
    ctx = { 'pickdata': pickdata,
            'today': today,
            'today_con': today_con}
    return render(request, 'pick.html', ctx)

def yesterday_pick(request, yesterday_con, yesterday_venue):
    dt_today = datetime.datetime.now()
    dt_yesterday = dt_today - datetime.timedelta(days=1)
    yesterday = dt_yesterday.strftime('%Y/%m/%d')
    pickdata = NarModel.objects.filter(開催日=yesterday, 開催場所=yesterday_venue).values()
    ctx = { 'pickdata': pickdata,
            'yesterday': yesterday,
            'yesterday_con': yesterday_con}
    return render(request, 'pick.html', ctx)

def tomorrow_pick(request, tomorrow_con, tomorrow_venue):
    dt_today = datetime.datetime.now()
    dt_tomorrow = dt_today - datetime.timedelta(days=-1)
    tomorrow = dt_tomorrow.strftime('%Y/%m/%d')
    pickdata = NarModel.objects.filter(開催日=tomorrow, 開催場所=tomorrow_venue).values()
    ctx = { 'pickdata': pickdata,
            'tomorrow': tomorrow,
            'tomorrow_con': tomorrow_con}
    return render(request, 'pick.html', ctx)





    # def sample(request):
    #     helddata = NarModel.objects.values('開催日', '開催場所').distinct()
    #     helddata = {
    #         'helddata': helddata,
    #     }
    #     return render(request, 'home.html', helddata)

class SortView(ListView):
    model = NarModel
    template_name = 'sort.html'
    
# class DeleteView(DeleteView):
#     model = NarModel
#     template_name = 'delete.html'
#     success_url = reverse_lazy('pick')

        # ctx['today_venue'] = NarModel.objects.filter(開催日=today).values('開催場所').distinct()
        # ctx['yesterday_venue'] = NarModel.objects.filter(開催日=yesterday).values('開催場所').distinct()
        # ctx['tomorrow_venue'] = NarModel.objects.filter(開催日=tomorrow).values('開催場所').distinct()