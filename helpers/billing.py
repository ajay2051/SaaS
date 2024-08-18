import stripe

stripe.api_key = "sk_test_4eC39HqLyjWDarjtT1zdp7dc"


def create_customer(name="", email="", raw=False):
    response = stripe.Customer.create(
        name=name,
        email=email,
    )
    if raw:
        return response
    return response.id  # stripe id


def create_product(name, metadata={}, raw=False):
    response = stripe.Product.create(name=name, metadata=metadata)
    if raw:
        return response
    stripe_id = response.id
    return stripe_id


def create_price(currency, unit_amount, recurring, product, raw=False):
    if product is None:
        return None
    response = stripe.Price.create(currency=currency, unit_amount=unit_amount, recurring=recurring, product=product, raw=False)
    if raw:
        return response
    stripe_id = response.id
    return stripe_id
