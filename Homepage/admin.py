from django.contrib import admin
from .models import *

Models = [Profile, Category, Customer, Order, Employee, Owner, Game, Coupon, Basket, Food, BasketFood]
admin.site.register(Models)


class TableAdmin(admin.ModelAdmin):
    readonly_fields = ('remaining_capacity',)


admin.site.register(Table, TableAdmin)


class Game_TimeAdmin(admin.ModelAdmin):
    readonly_fields = ('total_price',)


admin.site.register(Game_Time, Game_TimeAdmin)
# def price_game_time() :
#     M = end - start
#     M = M *
#     M = int(M)
#     if end - start > 0 :
#         return (M * 200 + "Toman")
