'''
Robert Penner's Easing Equations in Python. `source`_

.. _source: http://gist.github.com/dyyybek/d2041ae130a8a573d46aee5542d92bf1

- t = current time
- b = start value
- c = change in value
- d = duration

'''

from __future__ import division
import math

def linearTween(t, b, c, d):
    return c * t / d + b

# -------
# ease in
# -------

def easeInSine(t, b, c, d):
    return -c * math.cos(t / d * (math.pi / 2)) + c + b

def easeInQuad(t, b, c, d):
    t /= d
    return c * t * t + b

def easeInCubic(t, b, c, d):
    t /= d
    return c * t * t * t + b

def easeInQuart(t, b, c, d):
    t /= d
    return c * t * t * t * t + b

def easeInQuint(t, b, c, d):
    t /= d
    return c * t * t * t * t * t + b

def easeInCirc(t, b, c, d):
    t /= d
    return -c * (math.sqrt(1 - t * t) - 1) + b

def easeInExpo(t, b, c, d):
    return c * math.pow(2, 10 * (t / d - 1) ) + b

# --------
# ease out
# --------

def easeOutSine(t, b, c, d):
    return c * math.sin(t / d * (math.pi / 2)) + b

def easeOutQuad(t, b, c, d):
    t /= d
    return -c * t * (t - 2) + b

def easeOutCubic(t, b, c, d):
    t = t / d - 1
    return c * (t * t * t + 1) + b


def easeOutQuart(t, b, c, d):
    t /= d
    t -= 1
    return -c * (t * t * t * t - 1) + b

def easeOutQuint(t, b, c, d):
    t /= d
    t -= 1
    return c * (t * t * t * t * t + 1) + b

def easeOutCirc(t, b, c, d):
    t /= d
    t -= 1
    return c * math.sqrt(1 - t * t) + b

def easeOutExpo(t, b, c, d):
    return c * (-math.pow(2, -10 * t / d) + 1 ) + b

# -----------
# ease in/out
# -----------

def easeInOutSine(t, b, c, d):
    return -c / 2 * (math.cos(math.pi * t / d) - 1) + b

def easeInOutQuad(t, b, c, d):
    t /= d / 2
    if t < 1:
        return c / 2 * t * t + b
    t -= 1
    return -c / 2 * (t * (t - 2) - 1) + b

def easeInOutCubic(t, b, c, d):
    t /= d / 2
    if t < 1:
        return c / 2 * t * t * t + b
    t -= 2
    return c / 2 * (t * t * t + 2) + b

def easeInOutQuart(t, b, c, d):
    t /= d / 2
    if t < 1:
        return c / 2 * t * t * t * t + b
    t -= 2
    return -c / 2 * (t * t * t * t - 2) + b

def easeInOutQuint(t, b, c, d):
    t /= d / 2
    if t < 1:
        return c / 2 * t * t * t * t * t + b
    t -= 2
    return c / 2 * (t * t * t * t * t + 2) + b

def easeInOutCirc(t, b, c, d):
    t /= d/2.
    if t < 1:
        return -c/2 * (math.sqrt(1 - t*t) - 1) + b
    t -= 2
    return c/2 * (math.sqrt(1 - t*t) + 1) + b

def easeInOutExpo(t, b, c, d):
    t /= d / 2.
    if t < 1:
        return c / 2 * math.pow( 2, 10 * (t - 1) ) + b
    t -= 1
    return c / 2 * (-math.pow( 2, -10 * t) + 2 ) + b

