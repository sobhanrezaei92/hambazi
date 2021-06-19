from django.db import models
from djangoProject1 import settings
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True)
    location = models.CharField(max_length=150, blank=True, null=True)
    birth_date = models.DateTimeField(blank=True, null=True)
    bio = models.TextField(max_length=500, blank=True, null=True)
    is_employee = models.BooleanField(blank=True, null=True)
    is_owner = models.BooleanField(blank=True, null=True)
    Favorite_games = models.TextField(max_length=150, blank=True, null=True)

    def __str__(self):
        return self.user.username


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance).save()


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


class Category(models.Model):
    name = models.CharField(max_length=20)
    description = models.TextField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    slug = models.CharField(max_length=10, blank=True, null=True)

    def __str__(self):
        return self.name


class Game(models.Model):
    name = models.CharField(max_length=20)
    information = models.TextField(max_length=100, blank=True, null=True)
    description = models.TextField(max_length=50, blank=True, null=True)
    category = models.ManyToManyField(Category)
    store_inventory = models.IntegerField(default=0)
    is_available = models.BooleanField()
    price = models.IntegerField(blank=True, null=True)
    rent_per_minute = models.IntegerField()

    def __str__(self):
        return self.name


class Customer(models.Model):
    games = models.ManyToManyField(Game, through='Game_Time')
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)

    def __str__(self):
        return self.profile.user.username


class Table(models.Model):
    table_number = models.IntegerField()
    capacity = models.IntegerField()
    current_capacity = models.IntegerField()
    is_available = models.BooleanField()

    def calculate_capacity(self):
        if self.capacity == self.current_capacity:
            return "Capacity is complete"
        else:
            return int(self.capacity - self.current_capacity)

    remaining_capacity = property(calculate_capacity)


class Coupon(models.Model):
    name = models.CharField(max_length=15, blank=True, null=True)
    expire_date = models.DateTimeField(blank=True, null=True)
    value = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    description = models.CharField(max_length=30, blank=True, null=True)
    usage_count = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.name


class Order(models.Model):
    coupon = models.OneToOneField(Coupon, on_delete=models.CASCADE, blank=True, null=True)
    tip = models.IntegerField(default=0)
    table = models.ForeignKey(Table, on_delete=models.CASCADE)
    how_to_pay = models.CharField(choices=settings.HOW_TO_PAY, default='cash', max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_paid = models.BooleanField(default=False)
    Amount_of_cash_payment = models.IntegerField(default=0)
    Card_payment_amount = models.IntegerField(default=0)
    discount = models.IntegerField(default=0)  # mablaghi ke dasti vared mishe be onvane takhfif

    def calculate_order(self):
        if self.id:
            baskets_order = self.baskets.all()
            amount = 0
            if baskets_order:
                for basket in baskets_order:
                    if self.coupon.value == 0:
                        amount += int(basket.calculate_price_basket())
                    else:
                        amount += int(basket.calculate_price_basket())
            if self.coupon:
                amount -= int(self.coupon.value)
            else:
                amount = amount + int(self.tip) - int(self.discount)
            if self.Amount_of_cash_payment + self.Card_payment_amount == amount:
                self.is_paid = True
            else:
                self.is_paid = False
            if self.Amount_of_cash_payment == 0:
                self.how_to_pay = 'card'
            elif self.Card_payment_amount == 0:
                self.how_to_pay = 'cash'
            else:
                self.how_to_pay = 'cash,card'
            return amount

    total_order = property(calculate_order)

    # class Basket(models.Model):
    # customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    # coupon = models.OneToOneField(Coupon, on_delete=models.CASCADE, blank=True, null=True)
    # orders = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='baskets')

    # def calculate_price_basket(self):
    # basket_foods = self.basketfood_set.all()
    # basket_games = self.basketgame_set.all()
    # game_times = self.game_time_set.all()
    # total_basket_food = 0
    # total_basket_game = 0
    # total_game_time = 0
    # for basket_food in basket_foods:
    # total_basket_food += basket_food.food.sales_price * basket_food.number_of
    # for basket_game in basket_games:
    # total_basket_game += basket_game.game.price * basket_game.number_of
    # for game_time in game_times:
    # total_game_time += game_time.total_price

    # return total_basket_food + total_basket_game + total_game_time

    # total_basket = property(calculate_price_basket)

    # def __str__(self):
    # return self.customer.profile.user.username


class Game_Time(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # basket = models.ManyToManyField(Basket, )
    
    def calculate_total_price(self):
        if self.id:
            return int((self.end_time - self.start_time).seconds) / 60 * self.game.rent_per_minute
        else:
            return 0

    total_price = property(calculate_total_price)

    def __str__(self):
        return self.customer.profile.user.username


class Employee(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)

    def __str__(self):
        return self.profile.user.username


class Owner(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)


class Food(models.Model):
    name = models.CharField(max_length=20)
    description = models.TextField(max_length=75, blank=True, null=True)
    sales_price = models.IntegerField()  # gheymate furush
    purchase_price = models.IntegerField(blank=True, null=True)  # gheymate kharid
    created_at = models.DateTimeField(auto_now_add=True)  # khudesh besaze moghe'e avalin bar
    updated_at = models.DateTimeField(auto_now=True)  # khudesh update kone har bar ke save shod
    is_available = models.BooleanField()

    # basket = models.ManyToManyField(Basket, through='BasketFood')

    def __str__(self):
        return self.name


class BasketFood(models.Model):
    number_of = models.IntegerField()
    # basket = models.ForeignKey(Basket, on_delete=models.CASCADE)
    food = models.ForeignKey(Food, on_delete=models.CASCADE)


class BasketGame(models.Model):
    number_of = models.IntegerField()
    # basket = models.ForeignKey(Basket, on_delete=models.CASCADE)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)

    def calculate_basket_game(self):
        return self.number_of * self.game.price
    
    value = property(calculate_basket_game())


class Line_items(models.Model):
    id_line_items = models.IntegerField()
    basket_food = models.ForeignKey(BasketFood, on_delete=models.CASCADE)
    basket_game = models.ForeignKey(BasketGame, on_delete=models.CASCADE)
    game_time = models.ForeignKey(Game_Time, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)

    def claculate_Line_items(self):
        total_basket_food = BasketFood.objects.all()
        total_basket_game = BasketGame.objects.all()
        total_game_time = Game_Time.objects.all()
        amount = 0
        if BasketFood in Line_items:
            for total_basket_food in total_basket_foods:
                amount += self.BasketFood
        elif Game in Line_items:
            for total_basket_game in total_basket_games:
                amount += self.BasketGame
        elif Game_Time in Line_items:
            for total_game_time in total_game_times:
                amount += self.Game_Time
        return amount
