import math
import random

import numpy
from cv2 import cv2

def drawCircle(img, pos, color=(0, 0, 0)):
    x, y = pos.x, pos.y
    h, w, c = img.shape
    cx, cy = int(x * w), int(y * h)
    cv2.circle(img, (cx, cy), 3, color, cv2.FILLED)


def drawHearth(img, pos, r=15, color=(138, 0, 255)):
    x, y = pos.x, pos.y
    cv2.ellipse(img, (x, y), (r, r), 0, 180, 360, color, -1)
    cv2.ellipse(img, (x + 2 * r, y), (r, r), 0, 180, 360, color, -1)
    cv2.drawContours(img, [numpy.array([(x - r, y), (x + r, y + 2 * r), (x + 3 * r, y)])], 0, color, -1)


def drawText(img, p, text, color=(0, 0, 0)):
    x, y = p.x, p.y
    h, w, c = img.shape
    cx, cy = int(x * w), int(y * h)
    cv2.putText(img, text, (cx, cy), cv2.FONT_ITALIC, 1, color=color)


def drawLine(img, p1, p2, color=(0, 0, 0)):
    x1, y1 = p1.x, p1.y
    x2, y2 = p2.x, p2.y
    h, w, c = img.shape
    cx1, cy1 = int(x1 * w), int(y1 * h)
    cx2, cy2 = int(x2 * w), int(y2 * h)
    cv2.line(img, (cx1, cy1), (cx2, cy2), color=color)


def distance(p1, p2):
    return math.sqrt((p1.x - p2.x) ** 2 + (p1.y - p2.y) ** 2)


def mid(p1, p2):
    return Point((p1.x + p2.x) / 2, (p1.y + p2.y) / 2)


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class DestroyableCircle:
    def __init__(self, cx, cy, r, bomb=False):
        self.cx = cx
        self.cy = cy
        self.r = r
        self.isBomb = bomb

    def isInArea(self, x, y):
        return distance(Point(x, y), Point(self.cx, self.cy)) < ((self.r + 15))

    def draw(self, img):
        if self.isBomb:
            color = (127, 255, 127)
        else:
            color = (0, 0, 255)
        cv2.circle(img, (self.cx, self.cy), self.r, color, thickness=cv2.FILLED)


class DestroyableRect:
    def __init__(self, cx, cy, r, bomb=False):
        self.cx = cx
        self.cy = cy
        self.r = r
        self.isBomb = bomb

    def isInArea(self, x, y):
        if self.cx - (self.r + 15) > x:
            return False
        if self.cx + (self.r + 15) < x:
            return False
        if self.cy - (self.r + 15) > y:
            return False
        if self.cy + (self.r + 15) < y:
            return False
        return True

    def draw(self, img):
        if self.isBomb:
            color = (0, 0, 255)
        else:
            color = (127, 255, 127)
        cv2.rectangle(img, (self.cx - self.r, self.cy - self.r), (self.cx + self.r, self.cy + self.r),
                      color, thickness=cv2.FILLED)


class FixedStack:
    def __init__(self, maxsize):
        self.items = []
        self.maxSize = maxsize

    def isEmpty(self):
        return self.items == []

    def push(self, item):
        self.items.append(item)
        if len(self.items) == self.maxSize:
            self.pop()

    def pop(self):
        return self.items.pop(0)

    def peek(self):
        return self.items[0]

    def size(self):
        return len(self.items)


def findDestroyables(x, y):
    from main import destroyables
    for obj in destroyables:
        if obj.isInArea(x, y):
            return obj
    return None
