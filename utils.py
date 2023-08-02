def parse_purchases(purchases: str) -> dict:
    cart = {}
    purchases = purchases.split('-')

    for purchase in purchases:
        quantity = int(purchase[1::])
        purchase_id = int(purchase[0])
        cart[purchase_id] = quantity
    
    return cart


def numbers_format(value):
    """Makes a good looking numbers format."""

    return '{:,}'.format(value).replace(',', ' ')
