def test_delete_order(client, user_token):
    headers = {"Authorization": f"Bearer {user_token}"}
    response = client.post(
        "/orders/",
        json={
            "user_id": 1,
            "items": [
                {
                    "product_name": "Switch",
                    "quantity": 1,
                    "price": 300.0,
                }
            ],
        },
        headers=headers,
    )

    assert response.status_code == 200, f"Error al crear: {response.text}"

    order_id = response.json()["id"]
    del_resp = client.delete(f"/orders/{order_id}", headers=headers)
    assert del_resp.status_code == 204
