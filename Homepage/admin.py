from django.contrib import admin
from .models import *

Models = [Profile, Category, Customer, Employee, Owner, Game, Coupon, Food, BasketFood]
admin.site.register(Models)


class TableAdmin(admin.ModelAdmin):
    readonly_fields = ('remaining_capacity',)


admin.site.register(Table, TableAdmin)


class Game_TimeAdmin(admin.ModelAdmin):
    readonly_fields = ('total_price',)


admin.site.register(Game_Time, Game_TimeAdmin)


class Total_BasketAdmin(admin.ModelAdmin):
    readonly_fields = ('total_basket',)


admin.site.register(Basket, Total_BasketAdmin)


class OrderAdmin(admin.ModelAdmin):
    readonly_fields = ('calculate_order',)


admin.site.register(Order, OrderAdmin)
