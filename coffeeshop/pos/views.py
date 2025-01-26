from django.shortcuts import render, get_object_or_404, redirect
from .models import Drink, Flavor, Topping, Size, Order
from django.http import HttpResponse
import pprint

# tax for Allegheny, PA : 7%
tax = 1.07


def front_page(request):
    request.session["order"] = []
    request.session["item_sequence"] = 0
    return render(request, "pos/front_page.html")


def drinklist(request):
    drink_list = Drink.objects.values
    context = {
        "drink_list": drink_list,
    }
    return render(request, "pos/drinklist.html", context)


def build(request, drink_id):
    if request.method == "POST":
        order = request.session.get("order", [])
        request.session["item_sequence"] += 1
        item_sequence = request.session["item_sequence"]

        selected_drink = request.POST.get("drink")
        drink = get_object_or_404(Drink, drink_name=selected_drink)
        selected_size = drink.size_set.get(pk=request.POST["size"])

        selected_flavors = request.POST.getlist("flavor")
        flavor_obs = Flavor.objects.filter(pk__in=selected_flavors)
        flav_prices = [
            {"name": flavor.flavor_name, "price": flavor.flavor_upcharge}
            for flavor in flavor_obs
        ]
        flav_cost_tot = sum(flavor["price"] for flavor in flav_prices)

        selected_toppings = request.POST.getlist("topping")
        topp_obs = Topping.objects.filter(pk__in=selected_toppings)
        topp_prices = [
            {"name": topping.topping_name, "price": topping.topping_upcharge}
            for topping in topp_obs
        ]
        topp_cost_tot = sum(topp["price"] for topp in topp_prices)

        quant = int(request.POST.get("quantity"))

        drink_tot = (flav_cost_tot + topp_cost_tot + selected_size.size_cost) * quant

        data = {
            "item_sequence": item_sequence,
            "drink": selected_drink,
            "size": selected_size.to_dict(),
            "flavors": flav_prices,
            "toppings": topp_prices,
            "quantity": quant,
            "total_cost": drink_tot,
        }
        order.append(data)
        request.session["order"] = order
        request.session.modified = True
        return render(request, "pos/success.html", {"data": data})
    else:
        drink = get_object_or_404(Drink.objects.filter(pk=drink_id))
        sizes = Size.objects.filter(drink=drink)
        flavors = Flavor.objects.all()
        toppings = Topping.objects.all()
        return render(
            request,
            "pos/build.html",
            {"drink": drink, "sizes": sizes, "flavor": flavors, "topping": toppings},
        )


def complete(request):
    subtot = 0
    order = request.session.get("order", [])
    for drink in order:
        subtot = subtot + float(drink["total_cost"])
    order_total = round(subtot * tax, 2)
    tax_amount = round(subtot * (tax - 1), 2)
    order.append({"subtot": subtot, "tax": tax_amount, "total": order_total})
    order_id = Order.objects.create(order_details=order)
    request.session["order"] = []
    request.session.modified = True

    return render(
        request,
        "pos/complete.html",
        {"order": order, "order_id": order_id},
    )


def quantities(request):
    if request.method == "POST":
        order = request.session.get("order", [])
        updated_order = []

        if "remove_drink" in request.POST:
            drink_to_remove = int(request.POST.get("remove_drink"))
            print(f"Received drink_to_remove: {drink_to_remove}")  # Debugging output
            if drink_to_remove:
                updated_order = [
                    drink
                    for drink in order
                    if drink["item_sequence"] != drink_to_remove
                ]
                request.session["order"] = updated_order
                request.session.modified = True
                return render(request, "pos/changesdone.html")

        else:

            for drink in order:
                drink_key = (
                    f"quantity_{drink['item_sequence']}"  # Use a unique key format
                )
                new_quantity = int(request.POST.get(drink_key, drink["quantity"]))

                drink["quantity"] = new_quantity
                drink["total_cost"] = new_quantity * (
                    drink["size"]["size_cost"]
                    + sum(f["price"] for f in drink["flavors"])
                    + sum(t["price"] for t in drink["toppings"])
                )
                updated_order.append(drink)

            request.session["order"] = updated_order
            request.session.modified = True

            return render(request, "pos/changesdone.html")
    else:
        return render(request, "pos/changes.html")


def changesdone(request):
    return render(request, "pos/changesdone.html")
