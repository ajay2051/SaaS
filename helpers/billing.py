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
