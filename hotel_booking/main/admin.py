from django.contrib import admin
from .models import *

admin.site.register(Hotel)
admin.site.register(GuestHouse)


class GuestHouseImageInLine(admin.TabularInline):
    model = GuestHouseImage
    max_num = 10
    min_num = 3


@admin.register(GuestHouse)
class VillaAdmin(admin.ModelAdmin):
    inlines = [GuestHouseImageInLine, ]


class HotelImageInLine(admin.TabularInline):
    model = HotelImage
    max_num = 10
    min_num = 3


@admin.register(Hotel)
class HotelAdmin(admin.ModelAdmin):
    inlines = [HotelImageInLine, ]






admin.site.register(Comment)