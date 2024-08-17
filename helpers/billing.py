import stripe
stripe.api_key = "sk_test_4eC39HqLyjWDarjtT1zdp7dc"
stripe.Customer.create(
    name="<NAME>",
    email="<EMAIL>",
)