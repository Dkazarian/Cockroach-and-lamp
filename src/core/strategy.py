class Strategy:
    
    def __init__(self, item):
        self.item = item

    def update(self):
        None

    def setup(self):
    	None

    def clear(self):
    	None

    def get_item(self):
        return self.item
        
    def handle_collission(self):
        None