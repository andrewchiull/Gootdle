color2Hue = {"red":      0 / 2,
            "yellow":  60 / 2,
            "green":  120 / 2,
            "blue":   180 / 2,
            "blue":   240 / 2,
            "purple": 300 / 2}


class SomeClass:
    def foo(self, color: str):
        return color2Hue[color]