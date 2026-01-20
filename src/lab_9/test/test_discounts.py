from unittest.mock import patch

import pytest
from hypothesis import given
from hypothesis import strategies as st

from src.lab_9.discounts import calculate_discount, process_order_with_discount


@pytest.mark.modulo9
@pytest.mark.parametrize(
    "num_orders, total_amount, expected_discount",
    [
        (0, 100, 0.0),  # Usuario nuevo: 0%
        (6, 100, 0.10),  # > 5 órdenes: 10%
        (11, 100, 0.15),  # > 10 órdenes: 15%
        (6, 600, 0.15),  # > 5 órdenes (10%) + VIP > 500 (5%): 15%
    ],
)
def test_discount_logic(num_orders, total_amount, expected_discount):
    assert calculate_discount(num_orders, total_amount) == expected_discount


@given(st.integers(min_value=0, max_value=100), st.floats(min_value=0, max_value=10000))
def test_discount_properties(num_orders, total_amount):
    discount = calculate_discount(num_orders, total_amount)

    assert 0.0 <= discount <= 1.0


def test_process_order_sends_email_using_mock():
    with patch("src.lab_9.discounts.send_email_notification") as mock_email:
        mock_email.return_value = True
        result = process_order_with_discount("test@user.com", 6, 100)

        assert result == 0.10
        assert mock_email.called
        mock_email.assert_called_once_with(
            "test@user.com", "¡Ganaste un 10.0% de descuento!"
        )
