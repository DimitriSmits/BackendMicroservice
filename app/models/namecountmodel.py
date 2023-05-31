class NameCountModel:
    def __init__(self, name, count):
        self.name = name
        self.count = count
    
    def __str__(self):
        return f"Name: {self.name}, Count: {self.count}"