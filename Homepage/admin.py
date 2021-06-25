from django.contrib import admin

from .models import *

Models = [Profile, Category, Customer, Employee, Owner, Game, Coupon, Food, BasketFood, Category_Food]
admin.site.register(Models)


class TableAdmin(admin.ModelAdmin):
    readonly_fields = ('remaining_capacity',)


admin.site.register(Table, TableAdmin)


class BasketGameAdmin(admin.ModelAdmin):
    readonly_fields = ('value_game',)


admin.site.register(BasketGame, BasketGameAdmin)


class Game_TimeAdmin(admin.ModelAdmin):
    readonly_fields = ('total_price',)


admin.site.register(Game_Time, Game_TimeAdmin)


class total_line_item_admin(admin.ModelAdmin):
    readonly_fields = ['value_line_item']


admin.site.register(Line_item, total_line_item_admin)


# class BasketGameInline(admin.TabularInline):
#     model = BasketGame
class Line_Items_Inline(admin.TabularInline):
    model = Line_item
    fields = ['basket_food', 'basket_game', 'game_time', 'order', ]


class OrderAdmin(admin.ModelAdmin):
    readonly_fields = ['calculate_order', 'how_to_pay', 'is_paid', 'remained_amount']
    inlines = [
        Line_Items_Inline,
    ]


admin.site.register(Order, OrderAdmin)
