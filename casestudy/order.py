class Order:
    def __init__(self, order_id=None, customer_id=None, order_date=None, total_price=0.0, shipping_address=''):
        self._order_id = order_id
        self._customer_id = customer_id
        self._order_date = order_date
        self._total_price = total_price
        self._shipping_address = shipping_address

    @property
    def order_id(self):
        return self._order_id

    @order_id.setter
    def order_id(self, value):
        self._order_id = value

    @property
    def customer_id(self):
        return self._customer_id

    @customer_id.setter
    def customer_id(self, value):
        self._customer_id = value

    @property
    def order_date(self):
        return self._order_date

    @order_date.setter
    def order_date(self, value):
        self._order_date = value

    @property
    def total_price(self):
        return self._total_price

    @total_price.setter
    def total_price(self, value):
        self._total_price = value

    @property
    def shipping_address(self):
        return self._shipping_address

    @shipping_address.setter
    def shipping_address(self, value):
        self._shipping_address = value

    def __repr__(self):
        return f"Order({self.order_id}, CustID={self.customer_id}, ₹{self.total_price})"
