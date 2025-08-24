class OrderItem:
    def __init__(self, order_item_id=None, order_id=None, product_id=None, quantity=0):
        self._order_item_id = order_item_id
        self._order_id = order_id
        self._product_id = product_id
        self._quantity = quantity

    @property
    def order_item_id(self):
        return self._order_item_id

    @order_item_id.setter
    def order_item_id(self, value):
        self._order_item_id = value

    @property
    def order_id(self):
        return self._order_id

    @order_id.setter
    def order_id(self, value):
        self._order_id = value

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
        return f"OrderItem({self.order_item_id}, OrderID={self.order_id}, ProdID={self.product_id}, Qty={self.quantity})"
