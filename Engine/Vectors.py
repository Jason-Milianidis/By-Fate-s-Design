from __future__ import annotations
from pygame import Vector2
from typing import Optional
import math
import random


class Vector:
    x: float = 0
    y: float = 0

    def __init__(self, __x: float, __y: float):
        self.x = __x
        self.y = __y

    def magnitude(self) -> float:
        return math.sqrt(self.x ** 2 + self.y ** 2)

    def get_direction(self) -> float:
        return math.degrees(math.atan2(self.y, self.x))

    def normalize(self, scale: float = 1) -> Vector:
        mag = self.magnitude()
        if mag == 0:
            self.x, self.y = 0, 0
            return self
        self.x /= mag
        self.y /= mag
        return self.scale(scale)

    def rotate(self, degrees: float) -> Vector:
        __dir = (self.get_direction() + degrees) % 360
        mag = self.magnitude()
        vec = direction(__dir)
        self.x, self.y = vec.x, vec.y
        self.scale(mag)
        return self

    def scale(self, scalar: float | (float, float)) -> Vector:
        if isinstance(scalar, tuple):
            s1 = scalar[0]
            s2 = scalar[1]
        else:
            s1 = s2 = scalar

        self.x *= s1
        self.y *= s2
        return self

    def distance(self, vec: Vector) -> float:
        dx = self.x - vec.x
        dy = self.y - vec.y
        return math.sqrt(dx**2 + dy**2)

    def add(self, vec: Vector) -> Vector:
        self.x += vec.x
        self.y += vec.y
        return self

    def sub(self, vec: Vector) -> Vector:
        self.x -= vec.x
        self.y -= vec.y
        return self

    def dot(self, vec: Vector) -> float:
        return self.x * vec.x + self.y * vec.y

    def cross(self, vec: Vector) -> float:
        return self.magnitude() * vec.magnitude() * math.sin(self.angle(vec))

    def angle(self, vec: Vector) -> float:
        if self.magnitude() == 0 or vec.magnitude() == 0:
            return 0
        dot = duplicate(self).dot(vec)
        return dot / (self.magnitude() * vec.magnitude())

    def save(self) -> str:
        return str(self.x)+"x"+str(self.y)


def direction(degrees: Optional[float] = None) -> Vector:
    if degrees is None:
        degrees = random.randrange(0, 360)
    vector = Vector(math.cos(math.radians(degrees)), math.sin(math.radians(degrees)))
    return vector


def duplicate(vector: Vector) -> Vector:
    return Vector(vector.x, vector.y)


def tuple_to_vector(__tuple: tuple) -> Vector:
    return Vector(__tuple[0], __tuple[1])


def to_vector2(vector: Vector) -> Vector2:
    return Vector2(vector.x, vector.y)


def to_tuple(vector: Vector) -> tuple:
    t = (vector.x, vector.y)
    return t


def point_to(__from: Vector, __to: Vector) -> Vector:
    return Vector(__to.x - __from.x, __to.y - __from.y)


def load_vector(args: str) -> Vector:
    vals = args.split("x")
    return Vector(float(vals[0]), float(vals[1]))


def map_value(value: float, min_a: float, max_a: float, min_b: float, max_b: float) -> float:
    return min_b + ((max_b - min_b) / (max_a - min_a)) * (value - min_a)
