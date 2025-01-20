from .views import tax


def current_order(request):
    order = request.session.get("order", [])
    subtot = 0
    for drink in order:
        subtot = subtot + float(drink["total_cost"])
    order_total = round(subtot * tax, 2)
    tax_amount = round(subtot * (tax - 1), 2)
    print(order)
    return {
        "current_order": order,
        "subtotal": subtot,
        "tax_amount": tax_amount,
        "order_total": order_total,
        "tax": ((tax - 1) * 100),
    }
