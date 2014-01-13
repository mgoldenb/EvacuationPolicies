"""The "Compliant" policy:.

.. moduleauthor:: Meir Goldenberg <mgoldenbe@gmail.com>

"""
class Compliant:
    """The Compliant class"""
    def __init__(self, path):
        self.color = 'cyan'
        self.path = path
        self.pos = 0
    
    def next(self):
        """Returns the location for the next time step"""
        if self.pos >= len(self.path)-1: return self.path[-1]
        return self.path[self.pos + 1]
    
    def feedback(self, succeededFlag):
        if succeededFlag: self.pos += 1
