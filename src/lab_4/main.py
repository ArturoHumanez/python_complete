from modelos import Order, OrderIn, OrderOut


def run_laboratorio():
    raw_data = {
        "customer_email": "usuario@ejemplo.com",
        "items": ["Laptop", "Mouse"],
        "price_per_item": 500.0,
    }

    try:
        # Validación con Pydantic
        validated_input = OrderIn(**raw_data)
        print("Datos de entrada validados correctamente.")

        # Conversión
        order_total = len(validated_input.items) * validated_input.price_per_item

        my_order = Order(order_id=101, items=validated_input.items, total=order_total)
        print(f"Entidad creada: {my_order}")
        print(f"Impuestos calculados: ${my_order.tax}")

        # Serialización
        response = OrderOut(
            order_id=my_order.order_id, total_with_tax=my_order.total + my_order.tax
        )
        print("Respuesta lista para enviar:")
        print(f" {response.model_dump_json(indent=2)}")

    except Exception as e:
        print(f"Error en el proceso: {e}")


if __name__ == "__main__":
    run_laboratorio()
