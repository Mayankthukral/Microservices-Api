# caps/model/caps_model.py

class Caps:
    def __init__(self, cap_id, cap_name, cap_price):
        self.cap_id = cap_id
        self.cap_name = cap_name
        self.cap_price = cap_price

    def to_dict(self):
        return {
            'cap_id': self.cap_id,
            'cap_name': self.cap_name,
            'cap_price': self.cap_price
        }
