
class Compliant:
    def __init__(self, path):
        self.color = 'cyan'
        self.path = path
        self.pos = 0
    
    def next(self):
        if self.pos >= len(self.path)-1: return self.path[-1]
        return self.path[self.pos + 1]
    
    def feedback(self, succeededFlag):
        if succeededFlag: self.pos += 1