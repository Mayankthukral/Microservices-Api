# trousers_model.py
class TrousersModel:
    def __init__(self, trousers_id, trousers_name, trousers_price):
        self.trousers_id = trousers_id
        self.trousers_name = trousers_name
        self.trousers_price = trousers_price

    def to_dict(self):
        return {
            'trousers_id': self.trousers_id,
            'trousers_name': self.trousers_name,
            'trousers_price': self.trousers_price,
            '_id': str(self._id)  # Convert ObjectId to string
        }
