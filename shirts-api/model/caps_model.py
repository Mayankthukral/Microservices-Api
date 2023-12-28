class ShirtsModel:
    def __init__(self, shirt_id, shirt_name, shirt_price):
        self.shirt_id = shirt_id
        self.shirt_name = shirt_name
        self.shirt_price = shirt_price

    def to_dict(self):
        return {
            'shirt_id': self.shirt_id,
            'shirt_name': self.shirt_name,
            'shirt_price': self.shirt_price,
            '_id': str(self._id)  # Convert ObjectId to string
        }
