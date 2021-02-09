import random

UNIFORM_DIST_MIN = 0
UNIFORM_DIST_MAX = 1


def get_latency_value(mean, std):
    return random.normalvariate(mean, std)


def check_anomaly(split):
    v = random.uniform(UNIFORM_DIST_MIN, UNIFORM_DIST_MAX)

    if v < split:
        return True
    return False
