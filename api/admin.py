from django.contrib import admin
from .models import User, Rider, Quote, Order, Invoice

admin.site.register(User)
admin.site.register(Rider)
admin.site.register(Quote)
admin.site.register(Order)
admin.site.register(Invoice)
