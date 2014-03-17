class Stack(list):
    def push(self, item):
        self.append(item)
    def isEmpty(self):
        return not self
