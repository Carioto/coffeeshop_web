from datetime import datetime
from django.db import models
from django.core.serializers.json import DjangoJSONEncoder


class Drink(models.Model):
    drink_name = models.CharField(max_length=20)

    def __str__(self):
        return self.drink_name

    def to_dict(self):
        return {
            "id": self.id,
            "drink_name": self.drink_name,
        }


class Size(models.Model):
    drink = models.ForeignKey(Drink, on_delete=models.CASCADE)
    size_name = models.CharField(max_length=20)
    size_cost = models.FloatField(default=1.00)

    def __str__(self):
        return self.size_name

    def to_dict(self):
        return {
            "id": self.id,
            "size_name": self.size_name,
            "size_cost": self.size_cost,
            "drink": self.drink.to_dict(),  # Include related Drink as a dictionary
        }


class Flavor(models.Model):
    flavor_name = models.CharField(max_length=20)
    flavor_upcharge = models.FloatField(default=0.00)

    def __str__(self):
        return self.flavor_name

    def to_dict(self):
        return {
            "id": self.id,
            "flavor_name": self.flavor_name,
            "flavor_upcharge": self.flavor_upcharge,
        }


class Topping(models.Model):
    topping_name = models.CharField(max_length=20)
    topping_upcharge = models.FloatField(default=0.00)

    def __str__(self):
        return self.topping_name

    def to_dict(self):
        return {
            "id": self.id,
            "topping_name": self.topping_name,
            "topping_upcharge": self.topping_upcharge,
        }


class CustomJSONEncoder(DjangoJSONEncoder):
    def default(self, obj):
        if hasattr(obj, "to_dict"):  # Use a `to_dict` method if available
            return obj.to_dict()
        elif isinstance(obj, datetime):
            return obj.isoformat()  # Serialize datetime objects
        return super().default(obj)


class Order(models.Model):
    order_date = models.DateTimeField(auto_now_add=True)
    order_details = models.JSONField(default=list, encoder=CustomJSONEncoder)

    def __str__(self):
        return f"Order #{self.id}"
