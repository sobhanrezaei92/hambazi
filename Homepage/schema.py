import graphene
from graphene import relay
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField

from .models import *


class GameNode(DjangoObjectType):
    class Meta:
        model = Game
        filter_fields = ["id"]
        interfaces = (relay.Node,)


class ProfileNode(DjangoObjectType):
    class Meta:
        model = Profile
        filter_fields = ["id"]
        interfaces = (relay.Node,)


class CategoryNode(DjangoObjectType):
    class Meta:
        model = Category
        filter_fields = ["name"]
        interfaces = (relay.Node,)


class CustomerNode(DjangoObjectType):
    class Meta:
        model = Customer
        filter_fields = ["id"]
        interfaces = (relay.Node,)


class TableNode(DjangoObjectType):
    class Meta:
        model = Table
        filter_fields = ["id", "table_number"]
        interfaces = (relay.Node,)


class CouponNode(DjangoObjectType):
    class Meta:
        model = Coupon
        filter_fields = ["id"]
        interfaces = (relay.Node,)


class OrderNode(DjangoObjectType):
    class Meta:
        model = Order
        filter_fields = ["id"]
        interfaces = (relay.Node,)


class GameTimeNode(DjangoObjectType):
    class Meta:
        model = Game_Time
        filter_fields = ["id"]
        interfaces = (relay.Node,)


class EmployeeNode(DjangoObjectType):
    class Meta:
        model = Employee
        filter_fields = ["id"]
        interfaces = (relay.Node,)


class OwnerNode(DjangoObjectType):
    class Meta:
        model = Owner
        filter_fields = ["id"]
        interfaces = (relay.Node,)


class CategoryFoodNode(DjangoObjectType):
    class Meta:
        model = Category_Food
        filter_fields = ["id", "name"]
        interfaces = (relay.Node,)


class FoodNode(DjangoObjectType):
    class Meta:
        model = Food
        filter_fields = ["id"]
        interfaces = (relay.Node,)


class BasketFoodNode(DjangoObjectType):
    class Meta:
        model = BasketFood
        filter_fields = ["id"]
        interfaces = (relay.Node,)


class BasketGameNode(DjangoObjectType):
    class Meta:
        model = BasketGame
        filter_fields = ["id"]
        interfaces = (relay.Node,)


class LineItemNode(DjangoObjectType):
    class Meta:
        model = Line_item
        filter_fields = ["id"]
        interfaces = (relay.Node,)


class Query(graphene.ObjectType):
    game = relay.Node.Field(GameNode)
    all_games = DjangoFilterConnectionField(GameNode)
    profile = relay.Node.Field(ProfileNode)
    all_profiles = DjangoFilterConnectionField(ProfileNode)
    category = relay.Node.Field(CategoryNode)
    all_categories = DjangoFilterConnectionField(CategoryNode)
    customer = relay.Node.Field(CustomerNode)
    all_customers = DjangoFilterConnectionField(CustomerNode)
    table = relay.Node.Field(TableNode)
    all_tables = DjangoFilterConnectionField(TableNode)
    coupon = relay.Node.Field(CouponNode)
    all_coupons = DjangoFilterConnectionField(CouponNode)
    order = relay.Node.Field(OrderNode)
    all_orders = DjangoFilterConnectionField(OrderNode)
    game_time = relay.Node.Field(GameTimeNode)
    all_game_times = DjangoFilterConnectionField(GameTimeNode)
    employee = relay.Node.Field(EmployeeNode)
    all_employees = DjangoFilterConnectionField(EmployeeNode)
    owner = relay.Node.Field(OwnerNode)
    all_owners = DjangoFilterConnectionField(OwnerNode)
    category_food = relay.Node.Field(CategoryFoodNode)
    all_category_foods = DjangoFilterConnectionField(CategoryFoodNode)
    food = relay.Node.Field(FoodNode)
    all_foods = DjangoFilterConnectionField(FoodNode)
    basketfood = relay.Node.Field(BasketFoodNode)
    all_basketfoods = DjangoFilterConnectionField(BasketFoodNode)
    basketgame = relay.Node.Field(BasketGameNode)
    all_basketgames = DjangoFilterConnectionField(BasketGameNode)
    line_item = relay.Node.Field(LineItemNode)
    all_line_items = DjangoFilterConnectionField(LineItemNode)