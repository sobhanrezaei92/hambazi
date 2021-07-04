import graphene
from graphene import relay
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from graphql_relay import from_global_id

from .models import *


class GameNode(DjangoObjectType):
    class Meta:
        model = Game
        filter_fields = ["id", "name"]
        interfaces = (relay.Node,)


class GameMutation(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)
        id = graphene.ID()

    game = graphene.Field(GameNode)

    @classmethod
    def mutate(cls, root, info, name, id):
        game = Game.objects.get(id=int(from_global_id(id)[1]))
        game.name = name
        game.save()

        return GameMutation(game=game)


class ProfileNode(DjangoObjectType):
    class Meta:
        model = Profile
        filter_fields = ["id"]
        interfaces = (relay.Node,)


class ProfileMutation(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)
        id = graphene.ID()

    profile = graphene.Field(ProfileNode)

    @classmethod
    def mutate(cls, root, info, name, id):
        profile = Profile.objects.get(id=int(from_global_id(id)[1]))
        profile.name = name
        profile.save()

        return ProfileMutation(profile=profile)


class CategoryNode(DjangoObjectType):
    class Meta:
        model = Category
        filter_fields = ["name"]
        interfaces = (relay.Node,)


class CategoryMutation(graphene.Mutation):
    class Arguments:
        name = graphene.String()
        id = graphene.ID(required=True)
        description = graphene.String()
        created_at = graphene.DateTime()
        updated_at = graphene.DateTime()
        slug = graphene.String()

    category = graphene.Field(CategoryNode)

    @classmethod
    def mutate(cls, root, info, name, description, created_at, updated_at, slug, id):
        category = Category.objects.get(id=int(from_global_id(id)[1]))
        if name:
            category.name = name
        if description:
            category.description = description
        if created_at:
            category.created_at = created_at
        if updated_at:
            category.updated_at = updated_at
        if slug:
            category.slug = slug
        category.save()

        return CategoryMutation(category=category)


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


class OrderMutation(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)
        coupon_id = graphene.ID(required=True)

    Order = graphene.Field(OrderNode)

    @classmethod
    def mutate(cls, root, info, id, coupon_id):
        order = Order.objects.get(id=int(from_global_id(id)[1]))
        coupon = Coupon.objects.get(id=int(from_global_id(coupon_id)[1]))
        order.coupon = coupon
        order.save()

        return OrderMutation(order=order)


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


class Mutation(graphene.ObjectType):
    update_game = GameMutation.Field()
    update_category = CategoryMutation.Field()
    update_order = OrderMutation.Field()
