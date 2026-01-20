def calculate_discount(num_orders: int, total_amount: float) -> float:
    discount = 0.0

    if num_orders > 10:
        discount = 0.15
    elif num_orders > 5:
        discount = 0.10

    if total_amount > 500:
        discount += 0.05

    return round(discount, 2)


def send_email_notification(email: str, message: str):
    print(f"Enviando mail real a {email}...")
    return True


def process_order_with_discount(email: str, num_orders: int, total_amount: float):
    discount = calculate_discount(num_orders, total_amount)

    if discount > 0:
        send_email_notification(email, f"¡Ganaste un {discount * 100}% de descuento!")

    return discount
