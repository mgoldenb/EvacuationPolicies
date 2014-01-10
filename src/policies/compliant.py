
class Compliant:
    def __init__(self, path):
        self.path = path
        self.pos = 0
    
    def next(self):
        return self.path[self.pos + 1]
    
    def feedback(self, succeededFlag):
        if succeededFlag: self.pos += 1