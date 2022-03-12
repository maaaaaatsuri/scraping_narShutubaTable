from django.contrib import admin
from .models import Venue
from .models import Jockey
from .models import Stable
from .models import Mark
from .models import RaceInfo
from .models import RaceTable
from .models import RaceResults


# Register your models here.

admin.site.register(Venue)
admin.site.register(Jockey)
admin.site.register(Stable)
admin.site.register(Mark)
admin.site.register(RaceInfo)
admin.site.register(RaceTable)
admin.site.register(RaceResults)