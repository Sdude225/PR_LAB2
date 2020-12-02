import random
import math

def is_prime(num):
    if num % 2 == 0:
        return False

    elif any(num % i == 0 for i in range(3, int(math.sqrt(num)) + 1, 2)):
        return False

    else:
        return True

def generate_prime():
    prime_list = [x for x in range(1000, 5000) if is_prime(x)]
    return random.choice(prime_list)
