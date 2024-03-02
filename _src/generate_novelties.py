"""
This program generates, what I call, the Novelties.
A member of the Novelties is called a novelty.
The Novelties use a non-positional number system where each novelty is represented
as a concatenation of the primes it is composed of; however the primes are
represented by the order in which they exist as primes.
For example: the number 1176, which has a prime factorization of (2^3)*(3)*(7^2),
would be written as a novelty as: 1-1-1-2-4-4, since 2 is the first prime, 3 is the
second, and 7 is the fourth.

The reasons for doing this are none; however, multiplication and division in the
Novelties is trivial.  In addition, novelties are invariant under permutation of
their "digits".
"""

import sieve_of_eratosthenes as soe
import usefull_prints as uprint

primes = soe.primes_up_to_100()


def prime_factorization(n):
    global primes
    local_primes = primes[:int(n ** 0.5) + 1]
    factors = {}
    for prime in local_primes:
        exponent = 0
        while n % prime == 0:
            exponent += 1
            n //= prime
        if exponent > 0:
            factors[prime] = exponent
        if n == 1:
            break
    if n > 1:
        factors[n] = 1

    return factors


def generate_single(value: int):
    """
    Converts a natural number into a novelty, returned as a string.
    :param value: natural number to convert into novelty string
    :return: novelty as a string
    """
    global primes
    # primes needs to be a list of all primes up to 'value'

    factors_dict = prime_factorization(value)  
    novelty_list = []
    for factor in factors_dict:
        prime_order = primes.index(factor) + 1
        exponent = factors_dict[factor]
        novelty_list += ([str(prime_order)] * exponent)

    novelty = '\u2022'.join(novelty_list)  # 2B58  00b7

    return novelty


def generate_up_to(max_value, display=False):
    global primes
    print(f'largest known prime: {primes[-1]}')
    primes = primes + soe.sieve_of_eratosthenes(max_value, primes[-1]) if max_value > primes[-1] and max_value > 100 \
        else primes
    print(primes)
    prime_ordinals = [i for i in range(1, len(primes) + 1)]
    if display:
        print('\nPrime to Prime Ordinal conversion chart:')
        uprint.multi_list_print([[0] + prime_ordinals, ['\'1\''] + primes],
                                ['Ordinal:', 'Prime:'],
                                cutoff=25, hbars=True, vbars='full', headings_every_row=True, universal_width=True)

    the_novelties = ['e']
    for i in range(2, max_value + 1):
        novelty = generate_single(i)
        # check for frauds

        the_novelties.append(novelty)

    if display:
        ordinals = [i for i in range(1, len(the_novelties) + 1)]
        print(f'\nThe Novelties up to {max_value}.\n')
        # uprint.column_print(the_novelties)
        uprint.multi_list_print([ordinals, the_novelties],
                                ['Natural:', 'Novelty:'],
                                cutoff=5, vbars='full', hbars=True, universal_width=True)
        print()


def main():
    generate_up_to(int(input("Input the largest number to reach: ")), True)


if __name__ == '__main__':
    main()
