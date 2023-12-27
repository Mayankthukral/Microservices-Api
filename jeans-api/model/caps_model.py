class JeansModel:
    def __init__(self, jeans_id, jeans_name, jeans_fit, jeans_price):
        self.jeans_id = jeans_id
        self.jeans_name = jeans_name
        self.jeans_fit = jeans_fit
        self.jeans_price = jeans_price

    def to_dict(self):
        return {
            'jeans_id': self.jeans_id,
            'jeans_name': self.jeans_name,
            'jeans_fit': self.jeans_fit,
            'jeans_price': self.jeans_price,
            '_id': str(self._id)  # Convert ObjectId to string
        }
