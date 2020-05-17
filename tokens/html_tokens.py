class TokenType:
    Opening = 'open'
    Closing = 'close'

class Token:

    def __init__(self, name, position, tp):
        self.name = name
        self.position = position
        self.type = tp

    def __str__(self):
        # if self.type == "open":
        #     return f'<{self.name}>'
        # elif self.type == "close":
        #     return f'</{self.name}>'
        #
        # else:
        #     return f'<{self.name}/>'
        return self.name

    def start(self):
        return self.position[0]

    def end(self):
        return self.position[1]