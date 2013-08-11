from django.contrib import admin
from food.models import Restaurant, Dish


class Foo(admin.TabularInline):
    model = Dish
    extra = 3


class RestAdmin(admin.ModelAdmin):
    fieldsets = [
        ("Added By", {'fields': ["user","date"]}),
        (None, {'fields': ['name']}),
        ('Location', {'fields': ['address', 'city', 'country', 'zipcode']})
    ]

    inlines = [Foo]

    list_display = ('name', 'city', 'country')

    list_filter = ['country', "city"]

    search_fields = ['name']


admin.site.register(Restaurant, RestAdmin)