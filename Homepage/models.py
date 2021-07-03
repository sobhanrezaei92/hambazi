from django.db import models
from django.db.models import Model

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
    price = models.IntegerField(default=0)
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
    remaining_capacity = models.IntegerField(default=0)

    def calculate_capacity(self):
        self.remaining_capacity = int(self.capacity - self.current_capacity)

    def save(self, *args, **kwargs):
        self.calculate_capacity()
        super().save(*args, **kwargs)

    def __str__(self):
        return " میز شماره" + str(self.table_number) + '، ' + str(self.capacity) + ' نفره'


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
    coupon = models.ForeignKey(Coupon, on_delete=models.CASCADE, blank=True, null=True)
    tip = models.IntegerField(default=0)
    table = models.ForeignKey(Table, on_delete=models.CASCADE)
    how_to_pay = models.CharField(choices=settings.HOW_TO_PAY, default='cash', max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_paid = models.BooleanField(default=False)
    Amount_of_cash_payment = models.IntegerField(default=0)
    Card_payment_amount = models.IntegerField(default=0)
    discount = models.IntegerField(default=0, blank=True, null=True)  # mablaghi ke dasti vared mishe be onvane takhfif
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, blank=True, null=True)
    guest = models.IntegerField(default=1)
    total_order = models.IntegerField(default=0)
    remained_amount = models.IntegerField(default=0)

    def calculate_order(self):
        amount = 0
        line_items_order = self.line_item_set.all()
        if line_items_order:
            for line_item in line_items_order:
                amount += int(line_item.value_line_item)

        amount += int(self.tip) - int(self.discount)
        if self.coupon:
            amount -= self.coupon.value
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
        self.total_order = amount

    def calculate_remained(self):
        self.remained_amount = self.total_order - (self.Card_payment_amount + self.Amount_of_cash_payment)

    def save(self, *args, **kwargs):
        self.calculate_order()
        self.calculate_remained()
        super().save(*args, **kwargs)

    def __str__(self):
        return "Order" + ' ' + str(self.customer.profile.user.username)


@receiver(post_save, sender=Order)
def save_table(sender, instance, **kwargs):
    instance.table.current_capacity = instance.guest
    instance.table.save()


class Game_Time(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    number_of_players = models.IntegerField(default=1)
    total_price = models.IntegerField(default=0)

    def calculate_total_price(self):
        self.total_price = int(int((
                                           self.end_time - self.start_time).seconds) / 60 * self.game.rent_per_minute * self.number_of_players)

    def save(self, *args, **kwargs):
        self.calculate_total_price()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.customer.profile.user.username


class Employee(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)

    def __str__(self):
        return self.profile.user.username


class Owner(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)

    def __str__(self):
        return self.profile.user.username


class Category_Food(models.Model):
    name = models.CharField(max_length=15)
    description = models.TextField(max_length=50, blank=True, null=True)
    crated_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    slug = models.CharField(max_length=10, blank=True, null=True)

    def __str__(self):
        return self.name


class Food(models.Model):
    name = models.CharField(max_length=20)
    description = models.TextField(max_length=75, blank=True, null=True)
    sales_price = models.IntegerField(default=0, blank=True, null=True)  # gheymate furush
    purchase_price = models.IntegerField(blank=True, null=True, default=0)  # gheymate kharid
    created_at = models.DateTimeField(auto_now_add=True)  # khudesh besaze moghe'e avalin bar
    updated_at = models.DateTimeField(auto_now=True)  # khudesh update kone har bar ke save shod
    is_available = models.BooleanField(blank=True, null=True)

    category_food = models.ForeignKey(Category_Food, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class BasketFood(models.Model):
    number_of = models.IntegerField()
    food = models.ForeignKey(Food, on_delete=models.CASCADE)
    value_food = models.IntegerField(default=0)

    def calculate_basket_food(self):
        self.value_food = int(self.number_of * self.food.sales_price)

    def save(self, *args, **kwargs):
        self.calculate_basket_food()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.food.name


class BasketGame(models.Model):
    number_of = models.IntegerField()
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    value_game = models.IntegerField(default=0)

    def calculate_basket_game(self):
        amount = self.number_of * self.game.price
        self.value_game = amount

    def save(self, *args, **kwargs):
        self.calculate_basket_game()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.game.name + ' ' + str(self.number_of)


class Line_item(models.Model):
    basket_food = models.ForeignKey(BasketFood, on_delete=models.CASCADE, blank=True, null=True)
    basket_game = models.ForeignKey(BasketGame, on_delete=models.CASCADE, blank=True, null=True)
    game_time = models.ForeignKey(Game_Time, on_delete=models.CASCADE, blank=True, null=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    value_line_item = models.IntegerField(default=0)

    def claculate_Line_items(self):
        total_basket_foods = BasketFood.objects.filter(line_item=self).all()
        total_basket_games = BasketGame.objects.filter(line_item=self).all()
        total_game_times = Game_Time.objects.filter(line_item=self).all()
        amount = 0
        if total_basket_foods:
            for total_basket_food in total_basket_foods:
                amount += total_basket_food.value_food
        if total_basket_games:
            for total_basket_game in total_basket_games:
                amount += total_basket_game.value_game
        if total_game_times:  # else
            for total_game_time in total_game_times:
                amount += total_game_time.total_price
        self.value_line_item = amount

    def save(self, *args, **kwargs):
        self.claculate_Line_items()
        super().save(*args, **kwargs)
