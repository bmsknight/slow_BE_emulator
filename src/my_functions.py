import random
import math

UNIFORM_DIST_MIN = 0
UNIFORM_DIST_MAX = 1


def get_latency_value(mean, std):
    return random.normalvariate(mean, std)


def check_anomaly(split):
    v = random.uniform(UNIFORM_DIST_MIN, UNIFORM_DIST_MAX)

    if v < split:
        return True
    return False


def compute_prime(num):
    prime_list = []
    for count in range(num+1):
        isprime = True

        for x in range(2, int(math.sqrt(count) + 1)):
            if count % x == 0:
                isprime = False
                break

        if isprime:
            prime_list.append(count)

    return prime_list
