class Cart:
    def __init__(self, cart_id=None, customer_id=None, product_id=None, quantity=0):
        self._cart_id = cart_id
        self._customer_id = customer_id
        self._product_id = product_id
        self._quantity = quantity

    @property
    def cart_id(self):
        return self._cart_id

    @cart_id.setter
    def cart_id(self, value):
        self._cart_id = value

    @property
    def customer_id(self):
        return self._customer_id

    @customer_id.setter
    def customer_id(self, value):
        self._customer_id = value

    @property
    def product_id(self):
        return self._product_id

    @product_id.setter
    def product_id(self, value):
        self._product_id = value

    @property
    def quantity(self):
        return self._quantity

    @quantity.setter
    def quantity(self, value):
        self._quantity = value

    def __repr__(self):
        return f"Cart({self.cart_id}, CustID={self.customer_id}, ProdID={self.product_id}, Qty={self.quantity})"
