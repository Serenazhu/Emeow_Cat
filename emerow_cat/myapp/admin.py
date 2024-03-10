from django.contrib import admin
from .models import Businesses, Representatives, Inbox, Sent

# Register your models here.
admin.site.register(Businesses)
admin.site.register(Representatives)
admin.site.register(Inbox)
admin.site.register(Sent)
