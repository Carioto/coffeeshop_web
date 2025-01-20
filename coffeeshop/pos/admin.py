from django.contrib import admin

from .models import Drink, Flavor, Topping, Size, Order


class SizeInline(admin.TabularInline):
    model = Size
    extra = 3


class DrinkAdmin(admin.ModelAdmin):
    fieldsets = [(None, {"fields": ["drink_name"]})]
    inlines = [SizeInline]


admin.site.register(Drink, DrinkAdmin)
admin.site.register(Flavor)
admin.site.register(Topping)
admin.site.register(Order)
