import graphene
from graphene import relay
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from graphql_relay import from_global_id

from .models import *


class ProfileNode(DjangoObjectType):
    class Meta:
        model = Profile
        filter_fields = ["id"]
        interfaces = (relay.Node,)


class ProfileInput(graphene.InputObjectType):
    # user = graphene.AbstractType()
    location = graphene.String()
    birth_date = graphene.DateTime()
    bio = graphene.String()
    is_employee = graphene.Boolean()
    is_owner = graphene.Boolean()
    Favorite_games = graphene.String()


class ProfileMutation(graphene.Mutation):
    class Arguments:
        name = graphene.String()
        id = graphene.ID(required=True)
        # user = graphene.AbstractType()
        location = graphene.String()
        birth_date = graphene.DateTime()
        bio = graphene.String()
        is_employee = graphene.Boolean()
        is_owner = graphene.Boolean()
        favorite_games = graphene.String()
        profile = graphene.Argument(ProfileInput)

    profile = graphene.Field(ProfileNode)

    @classmethod
    def mutate(cls, root, info, name, id, location, birth_date, bio, is_employee, is_owner, favorite_games):
        profile = Profile.objects.get(id=int(from_global_id(id)[1]))
        if name:
            profile.name = name
        # if user:
        # profile.user = user
        if location:
            profile.location = location
        if birth_date:
            profile.birth_date = birth_date
        if bio:
            profile.bio = bio
        if is_employee:
            profile.is_employee = is_employee
        if is_owner:
            profile.is_owner = is_owner
        if favorite_games:
            profile.Favorite_games = favorite_games
        profile.save()

        return ProfileMutation(profile=profile)


class CategoryNode(DjangoObjectType):
    class Meta:
        model = Category
        filter_fields = ["name"]
        interfaces = (relay.Node,)


class CategoryInput(graphene.InputObjectType):
    name = graphene.String()
    description = graphene.String()
    created_at = graphene.DateTime()
    updated_at = graphene.DateTime()
    slug = graphene.String()


class CategoryMutation(graphene.Mutation):
    class Arguments:
        name = graphene.String()
        id = graphene.ID(required=True)
        description = graphene.String()
        created_at = graphene.DateTime()
        updated_at = graphene.DateTime()
        slug = graphene.String()
        category = graphene.Argument(CategoryInput)

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


class GameNode(DjangoObjectType):
    class Meta:
        model = Game
        filter_fields = ["id", "name"]
        interfaces = (relay.Node,)


class GameInput(graphene.InputObjectType):
    name = graphene.String()
    information = graphene.String()
    description = graphene.String()
    category = graphene.List(CategoryInput)
    store_inventory = graphene.Int()
    is_available = graphene.Boolean()
    price = graphene.Int()
    rent_per_minute = graphene.Int()


class GameMutation(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)
        id = graphene.ID()
        information = graphene.String()
        description = graphene.String()
        category = graphene.List(CategoryInput)
        is_available = graphene.Boolean()
        store_inventory = graphene.Int()
        price = graphene.Int()
        rent_per_minute = graphene.Int()
        game = graphene.Argument(GameInput)

    game = graphene.Field(GameNode)

    @classmethod
    def mutate(cls, root, info, name, id, information, description, category, is_available,
               store_inventory, price, rent_per_minute, ):
        game = Game.objects.get(id=int(from_global_id(id)[1]))
        if name:
            game.name = name
        if information:
            game.information = information
        if description:
            game.description = description
        if category:
            game.category = category
        if is_available:
            game.is_available = is_available
        if store_inventory:
            game.store_inventory = store_inventory
        if price:
            game.price = price
        if rent_per_minute:
            game.rent_per_minute = rent_per_minute
        game.save()

        return GameMutation(game=game)


class CustomerNode(DjangoObjectType):
    class Meta:
        model = Customer
        filter_fields = ["id"]
        interfaces = (relay.Node,)


class CustomerInput(graphene.InputObjectType):
    games = graphene.List(GameInput)
    profile = graphene.List(ProfileInput)


class CustomerMutation(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)
        profile = graphene.List(ProfileInput)
        games = graphene.List(GameInput)
        customer = graphene.Argument(CustomerInput)

    customer = graphene.Field(CustomerNode)

    @classmethod
    def mutate(cls, root, info, profile, id, games):
        customer = Customer.objects.get(id=int(from_global_id(id)[1]))
        if profile:
            customer.profile = profile
        if games:
            customer.games = games
        customer.Save()
        return CustomerMutation(customer=customer)


class TableNode(DjangoObjectType):
    class Meta:
        model = Table
        filter_fields = ["id", "table_number"]
        interfaces = (relay.Node,)


class TableInput(graphene.InputObjectType):
    table_number = graphene.Int()
    capacity = graphene.Int()
    current_capacity = graphene.Int()
    is_available = graphene.Boolean()
    remaining_capacity = graphene.Int()


class TableMutation(graphene.Mutation):
    class Arguments:
        table_number = graphene.Int()
        id = graphene.ID(required=True)
        capacity = graphene.Int()
        current_capacity = graphene.Int()
        is_available = graphene.Boolean()
        remaining_capacity = graphene.Int()
        table = graphene.Argument(TableInput)

    table = graphene.Field(TableNode)

    @classmethod
    def mutate(cls, root, info, table_number, id, capacity, current_capacity, is_available, remaining_capacity, ):
        table = Table.objects.get(id=int(from_global_id(id)[1]))
        if table_number:
            table.table_number = table_number
        if capacity:
            table.capacity = capacity
        if current_capacity:
            table.current_capacity = current_capacity
        if is_available:
            table.is_available = is_available
        if remaining_capacity:
            table.remaining_capacity = remaining_capacity
        table.save()

        return TableMutation(table=table)


class CouponNode(DjangoObjectType):
    class Meta:
        model = Coupon
        filter_fields = ["id"]
        interfaces = (relay.Node,)


class CouponInput(graphene.InputObjectType):
    name = graphene.String()
    expire_date = graphene.DateTime()
    value = graphene.Int()
    created_at = graphene.DateTime()
    updated_at = graphene.DateTime()
    description = graphene.String()
    usage_count = graphene.Int()


class CouponMutation(graphene.Mutation):
    class Arguments:
        name = graphene.String()
        id = graphene.ID(required=True)
        expire_date = graphene.DateTime()
        value = graphene.Int()
        created_at = graphene.DateTime()
        updated_at = graphene.DateTime()
        description = graphene.String()
        usage_count = graphene.Int()
        coupon = graphene.Argument(CouponInput)

    coupon = graphene.Field(CouponNode)

    @classmethod
    def mutate(cls, root, info, name, id, expire_date, value, created_at, updated_at, description, usage_count):
        coupon = Coupon.objects.get(id=int(from_global_id(id)[1]))
        if name:
            coupon.name = name
        if expire_date:
            coupon.expire_date = expire_date
        if value:
            coupon.value = value
        if created_at:
            coupon.created_at = created_at
        if updated_at:
            coupon.updated_at = updated_at
        if description:
            coupon.description = description
        if usage_count:
            coupon.usage_count = usage_count

        coupon.save()

        return CouponMutation(coupon=coupon)


class OrderNode(DjangoObjectType):
    class Meta:
        model = Order
        filter_fields = ["id"]
        interfaces = (relay.Node,)


class OrderInput(graphene.InputObjectType):
    coupon = graphene.List(CouponInput)
    tip = graphene.Int()
    table = graphene.List(TableInput)
    how_to_pay = graphene.String()
    created_at = graphene.DateTime()
    updated_at = graphene.DateTime()
    is_paid = graphene.Boolean()
    Amount_of_cash_payment = graphene.Int()
    Card_payment_amount = graphene.Int()
    discount = graphene.Int()
    customer = graphene.List(CouponInput)
    guest = graphene.Int()
    total_order = graphene.Int()
    remained_amount = graphene.Int()


class OrderMutation(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)
        coupon_id = graphene.ID(required=True)
        coupon = graphene.List(CouponInput)
        tip = graphene.Int()
        table = graphene.List(TableInput)
        how_to_pay = graphene.String()
        created_at = graphene.DateTime()
        updated_at = graphene.DateTime()
        is_paid = graphene.Boolean()
        amount_of_cash_payment = graphene.Int()
        card_payment_amount = graphene.Int()
        discount = graphene.Int()
        customer = graphene.List(CustomerInput)
        guest = graphene.Int()
        total_order = graphene.Int()
        remained_amount = graphene.Int()
        order = graphene.Argument(OrderInput)

    Order = graphene.Field(OrderNode)

    @classmethod
    def mutate(cls, root, info, id, coupon_id, coupon, tip, table, how_to_pay, created_at, updated_at, is_paid,
               discount, customer, guest, total_order, remained_amount, amount_of_cash_payment, card_payment_amount, ):
        order = Order.objects.get(id=int(from_global_id(id)[1]))
        coupon = Coupon.objects.get(id=int(from_global_id(coupon_id)[1]))
        if coupon:
            order.coupon = coupon
        if tip:
            order.tip = tip
        if table:
            order.table = table
        if how_to_pay:
            order.how_to_pay = how_to_pay
        if created_at:
            order.created_at = created_at
        if updated_at:
            order.updated_at = updated_at
        if is_paid:
            order.is_paid = is_paid
        if amount_of_cash_payment:
            order.Amount_of_cash_payment = amount_of_cash_payment
        if card_payment_amount:
            order.Card_payment_amount = card_payment_amount
        if remained_amount:
            order.remained_amount = remained_amount
        if total_order:
            order.total_order = total_order
        if guest:
            order.guest = guest
        if customer:
            order.customer = customer
        if discount:
            order.discount = discount

        order.save()

        return OrderMutation(order=order)


class GameTimeNode(DjangoObjectType):
    class Meta:
        model = Game_Time
        filter_fields = ["id"]
        interfaces = (relay.Node,)


class GameTimeInput(graphene.InputObjectType):
    game = graphene.List(GameInput)
    customer = graphene.List(CustomerInput)
    start_time = graphene.DateTime()
    end_time = graphene.DateTime()
    created_at = graphene.DateTime()
    updated_at = graphene.DateTime()
    number_of_players = graphene.Int()
    total_price = graphene.Int()


class GameTimeMutation(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)
        game = graphene.List(GameInput)
        customer = graphene.List(CustomerInput)
        start_time = graphene.DateTime()
        end_time = graphene.DateTime()
        created_at = graphene.DateTime()
        updated_at = graphene.DateTime()
        number_of_players = graphene.Int()
        total_price = graphene.Int()
        game_time = graphene.Argument(GameTimeInput)

    gametime = graphene.Field(GameTimeNode)

    @classmethod
    def mutate(cls, root, info, id, game, customer, start_time,
               end_time, created_at, updated_at, number_of_players, total_price):
        gametime = Game_Time.objects.get(id=int(from_global_id(id)[1]))
        if game:
            gametime.game = game
        if customer:
            gametime.customer = customer
        if start_time:
            gametime.start_time = start_time
        if end_time:
            gametime.end_time = end_time
        if created_at:
            gametime.created_at = created_at
        if updated_at:
            gametime.updated_at = updated_at
        if number_of_players:
            gametime.number_of_players = number_of_players
        if total_price:
            gametime.total_price = total_price
        gametime.save()

        return GameTimeMutation(gametime=gametime)


class EmployeeNode(DjangoObjectType):
    class Meta:
        model = Employee
        filter_fields = ["id"]
        interfaces = (relay.Node,)


class EmployeeInput(graphene.InputObjectType):
    profile = graphene.List(ProfileInput)


class EmployeeMutation(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)
        profile = graphene.List(ProfileInput)
        employee = graphene.Argument(EmployeeInput)

    employee = graphene.Field(EmployeeNode)

    @classmethod
    def mutate(cls, root, info, id, profile, ):
        employee = Employee.objects.get(id=int(from_global_id(id)[1]))
        if profile:
            employee.profile = profile
        employee.save()

        return EmployeeMutation(employee=employee)


class OwnerNode(DjangoObjectType):
    class Meta:
        model = Owner
        filter_fields = ["id"]
        interfaces = (relay.Node,)


class OwnerInput(graphene.InputObjectType):
    profile = graphene.List(ProfileInput)


class OwnerMutation(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)
        profile = graphene.List(ProfileInput)
        owner = graphene.Argument(OwnerInput)

    owner = graphene.Field(OwnerNode)

    @classmethod
    def mutate(cls, root, info, id, profile, ):
        owner = Owner.objects.get(id=int(from_global_id(id)[1]))
        if profile:
            owner.profile = profile
        profile.save()

        return OwnerMutation(owner=owner)


class CategoryFoodNode(DjangoObjectType):
    class Meta:
        model = Category_Food
        filter_fields = ["id", "name"]
        interfaces = (relay.Node,)


class CategoryFoodInput(graphene.InputObjectType):
    name = graphene.String()
    description = graphene.String()
    crated_at = graphene.DateTime()
    updated_at = graphene.DateTime()
    slug = graphene.String()


class CategoryFoodMutation(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)
        name = graphene.String()
        description = graphene.String()
        created_at = graphene.DateTime()
        updated_at = graphene.DateTime()
        slug = graphene.String()
        category_food = graphene.Argument(CategoryFoodInput)

    category_food = graphene.Field(CategoryFoodNode)

    @classmethod
    def mutate(cls, root, info, id, name, description, created_at, updated_at, slug):
        category_food = Category_Food.objects.get(id=int(from_global_id(id)[1]))
        if name:
            category_food.name = name
        if description:
            category_food.description = description
        if created_at:
            category_food.crated_at = created_at
        if updated_at:
            category_food.updated_at = updated_at
        if slug:
            category_food.slug = slug
        category_food.save()

        return CategoryFoodMutation(category_food=category_food)


class FoodNode(DjangoObjectType):
    class Meta:
        model = Food
        filter_fields = ["id"]
        interfaces = (relay.Node,)


class FoodInput(graphene.InputObjectType):
    name = graphene.String()
    description = graphene.String()
    sales_price = graphene.Int()
    purchase_price = graphene.Int()
    created_at = graphene.DateTime()
    updated_at = graphene.DateTime()
    is_available = graphene.Boolean()
    category_food = graphene.List(CategoryFoodInput)


class FoodMutation(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)
        name = graphene.String()
        description = graphene.String()
        sales_price = graphene.Int()
        purchase_price = graphene.Int()
        created_at = graphene.DateTime()
        updated_at = graphene.DateTime()
        is_available = graphene.Boolean()
        category_food = graphene.List(CategoryFoodInput)
        food = graphene.Argument(FoodInput)

    food = graphene.Field(FoodNode)

    @classmethod
    def mutate(cls, root, info, id, name, description, sales_price, purchase_price,
               created_at, updated_at, is_available, category_food):
        food = Food.objects.get(id=int(from_global_id(id)[1]))
        if name:
            food.name = name
        if description:
            food.description = description
        if sales_price:
            food.sales_price = sales_price
        if purchase_price:
            food.purchase_price = purchase_price
        if created_at:
            food.created_at = created_at
        if updated_at:
            food.updated_at = updated_at
        if is_available:
            food.is_available = is_available
        if category_food:
            food.category_food = category_food
        food.save()

        return FoodMutation(food=food)


class BasketFoodNode(DjangoObjectType):
    class Meta:
        model = BasketFood
        filter_fields = ["id"]
        interfaces = (relay.Node,)


class BasketFoodInput(graphene.InputObjectType):
    number_of = graphene.Int()
    food = graphene.List(FoodInput)
    value_food = graphene.Int()


class BasketFoodMutation(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)
        number_of = graphene.Int()
        food = graphene.List(FoodInput)
        value_food = graphene.Int()
        basket_food = graphene.Argument(BasketFoodInput)

    basket_food = graphene.Field(BasketFoodNode)

    @classmethod
    def mutate(cls, root, info, id, number_of, food, value_food):
        basket_food = BasketFood.objects.get(id=int(from_global_id(id)[1]))
        if number_of:
            basket_food.number_of = number_of
        if food:
            basket_food.food = food
        if value_food:
            basket_food.value_food = value_food
        basket_food.save()

        return BasketFoodMutation(basket_food=basket_food)


class BasketGameNode(DjangoObjectType):
    class Meta:
        model = BasketGame
        filter_fields = ["id"]
        interfaces = (relay.Node,)


class BasketGameInput(graphene.InputObjectType):
    number_of = graphene.Int()
    game = graphene.List(GameInput)
    value_game = graphene.Int()


class BasketGameMutation(graphene.Mutation):
    class Arguments:
        id = graphene.ID()
        number_of = graphene.Int()
        game = graphene.List(GameInput)
        value_game = graphene.Int()
        basket_game = graphene.Argument(BasketGameInput)

    basket_game = graphene.Field(BasketGameNode)

    @classmethod
    def mutate(cls, root, info, id, number_of, game, value_game):
        basket_game = BasketGame.objects.get(id=int(from_global_id(id)[1]))
        if number_of:
            basket_game.number_of = number_of
        if game:
            basket_game.game = game
        if value_game:
            basket_game.value_game = value_game
        basket_game.save()

        return BasketGameMutation(basket_game=basket_game)


class LineItemNode(DjangoObjectType):
    class Meta:
        model = Line_item
        filter_fields = ["id"]
        interfaces = (relay.Node,)


class LineItemInput(graphene.InputObjectType):
    basket_food = graphene.List(BasketFoodInput)
    basket_game = graphene.List(BasketGameInput)
    game_time = graphene.List(GameTimeInput)
    order = graphene.List(OrderInput)
    value_line_item = graphene.Int()


class LineItemMutation(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)
        basket_food = graphene.List(BasketFoodInput)
        basket_game = graphene.List(BasketGameInput)
        game_time = graphene.List(GameTimeInput)
        order = graphene.List(OrderInput)
        value_line_item = graphene.Int()
        line_item = graphene.Argument(LineItemInput)

    line_item = graphene.Field(LineItemNode)

    @classmethod
    def mutate(cls, root, info, id, basket_food, basket_game, game_time, order, value_line_item):
        line_item = Line_item.objects.get(id=int(from_global_id(id)[1]))
        if basket_food:
            line_item.basket_food = basket_food
        if basket_game:
            line_item.basket_game = basket_game
        if game_time:
            line_item.game_time = game_time
        if order:
            line_item.order = order
        if value_line_item:
            line_item.value_line_item = value_line_item
        line_item.save()

        return LineItemMutation(line_item=line_item)


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
    update_profile = ProfileMutation.Field()
    update_category = CategoryMutation.Field()
    update_game = GameMutation.Field()
    update_customer = CustomerMutation.Field()
    update_table = TableMutation.Field()
    update_coupon = CouponMutation.Field()
    update_order = OrderMutation.Field()
    update_game_time = GameTimeMutation.Field()
    update_employee = EmployeeMutation.Field()
    update_owner = OwnerMutation.Field()
    update_category_food = CategoryFoodMutation.Field()
    update_food = FoodMutation.Field()
    update_basket_food = BasketFoodMutation.Field()
    update_basket_game = BasketGameMutation.Field()
    update_line_item = LineItemMutation.Field()
