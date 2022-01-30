from django.contrib import admin
from .models import MstVenue
from .models import MstJockey
from .models import MstStable
from .models import MstMark
from .models import RaceInfo
from .models import RaceTable
from .models import RaceResults


# Register your models here.

admin.site.register(MstVenue)
admin.site.register(MstJockey)
admin.site.register(MstStable)
admin.site.register(MstMark)
admin.site.register(RaceInfo)
admin.site.register(RaceTable)
admin.site.register(RaceResults)