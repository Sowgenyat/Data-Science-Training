class Product:
    def __init__(self, product_id=None, name='', price=0.0, description='', stock_quantity=0):
        self._product_id = product_id
        self._name = name
        self._price = price
        self._description = description
        self._stock_quantity = stock_quantity

    @property
    def product_id(self):
        return self._product_id

    @product_id.setter
    def product_id(self, value):
        self._product_id = value

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, value):
        self._price = value

    @property
    def description(self):
        return self._description

    @description.setter
    def description(self, value):
        self._description = value

    @property
    def stock_quantity(self):
        return self._stock_quantity

    @stock_quantity.setter
    def stock_quantity(self, value):
        self._stock_quantity = value

    def __repr__(self):
        return f"Product({self.product_id}, {self.name}, ₹{self.price})"
