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


# class Total_BasketAdmin(admin.ModelAdmin):
    # readonly_fields = ('total_basket',)
class total_line_item_admin(admin.ModelAdmin):
    readonly_fields = ['value_line_item']

admin.site.register(Line_item, total_line_item_admin)


class OrderAdmin(admin.ModelAdmin):
    readonly_fields = ['calculate_order',]


admin.site.register(Order, OrderAdmin)


class order_line_items(admin.TabularInline):
    model = Line_item
    readonly_fields = ['basket_food', 'basket_game', 'game_time', 'order',]