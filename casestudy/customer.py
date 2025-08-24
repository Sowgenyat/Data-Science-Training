class Customer:
    def __init__(self, customer_id=None, name='', email='', password=''):
        self._customer_id = customer_id
        self._name = name
        self._email = email
        self._password = password

    @property
    def customer_id(self):
        return self._customer_id

    @customer_id.setter
    def customer_id(self, value):
        self._customer_id = value

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, value):
        self._email = value

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, value):
        self._password = value

    def __repr__(self):
        return f"Customer({self.customer_id}, {self.name}, {self.email})"
