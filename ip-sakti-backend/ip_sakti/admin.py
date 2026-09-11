from django.contrib import admin

from ip_sakti.models import (
    State, GITag, Patent, BiopiracyCase, AYUSHFormulation,
    Alert, TKDL_Entry, DashboardStat, IPActivity,
)
from ip_sakti.users.models import User

admin.site.register([User, State, GITag, Patent, BiopiracyCase,
                     AYUSHFormulation, Alert, TKDL_Entry, DashboardStat,
                     IPActivity])
