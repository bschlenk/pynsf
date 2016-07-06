class Stack(list):
    """A fixed size stack"""
    def __init__(self, size=128):
        super(Stack, self).__init__()
        self.extend([0] * size)
        self.stack_size = size
        self.sp = 0

    def push(self, item):
        self[self.sp] = item
        self.sp += 1

    def pop(self):
        val = self[self.sp]
        self.sp -= 1
        return val

    def isEmpty(self):
        return not self

