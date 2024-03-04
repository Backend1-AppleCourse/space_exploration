
class Spaceship:
    def __init__(self, name, fuel, health, credit_points):
        self.name = name
        self.fuel = fuel
        self.health = health
        self.credit_points = credit_points

    def __str__(self):
        return f"Spaceship: {self.name}, Fuel: {self.fuel}, Health: {self.health}, CreditPoints: {self.credit_points}"