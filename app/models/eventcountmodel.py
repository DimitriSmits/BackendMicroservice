class EventCountModel:
    def __init__(self, name,month, count):
        self.name = name
        self.month = month
        self.count = count
    
    def __str__(self):
        return f"Name: {self.name}, Month: {self.month}, Count: {self.count}"