# The Novelties

This program generates, what I call, the Novelties.  A member of the Novelties is called a *novelty*. 

The Novelties use a non-positional number system where each novelty is represented as a concatenation of the primes it is composed of; however the primes are represented by the order in which they exist as primes.  

For example: the number 1176, which has a prime factorization of (2^3)(3)(7^2), would be written as a novelty as: 1-1-1-2-4-4, since 2 is the first prime, 3 is the second, and 7 is the fourth.

## Installation and Use

Python must be installed on your machine in order to run these modules.  This version runs through the command line and does not require any additional modules to be downloaded.

### Files
 - generate_novelties.py: Displays all the novelties from the natural number 1 up to the input value.
   Requires all three files to run.

 - sieve_of_eratosthenes.py: Finds all primes up to the input value.
   Can run on its own to show a visualization of the process (not recommened to input large numbers, lots of printing. n < 1000)
 
 - usefull_prints.py:  Module for printing lists in rows.
   Can run standalone to see examples of printing.

---

# Why?

Our understanding of quantities is based on an additive principle; where, to get from one number to the next, we add 1 (see the [Peano Axioms](https://youtu.be/3gBoP8jZ1Is?si=4pPOlf5IM-a0WDF2) for more details of this).  But this means that the essence of "one-ness" is found in having *one* thing, and "two-ness is having *one* thing and then having another *one* thing, and "three-ness" is having *one* thing, having another *one* thing and then having **another** *one* thing, ... ad nauseam.  If that is the case, then each number is essentially just a different bundle of ones.  The idea is to attribute **this** notion instead, to our understanding of oneness.  In fact, it is such an obvious way to think of numbers, we give it the special name of "identity", which we denote with "*e*".  This implies that the natural number 1 is equal to *e* as a novelty, or \( 1 := e \).

  The first *new* thing to encounter is having pairs of things, or pairs of *e*.  We could then learn everything there is to know about having different amounts of pairs of *e*.  Since this is the first novel thing we have discovered, it would makes sense to consider this as our new notion of "oneness" and give it the symbol, 1.
  The next new thing to encounter is having triples of *e*, and again we could learn all there is to know about triples of things.  It being the second novel thing, we call this notion, "two" and give it the symbol 2.  Now, it would seem that the next new thing would be to have quadruples. However, since a pair of pairs is 4 things, when we discovered pairs we also discovered quadruples. Since quintuples can not be reduced to pairs or triples, the next new thing will be: having quintuples of things. We call that "three" and give it the symbol, 3.  
 
  By the [Sieve of Eratosthenes](https://en.wikipedia.org/wiki/Sieve_of_Eratosthenes), we will only encounter new things when we encounter prime numbers.  In this expanded understanding of one-ness, two-ness, and so on, we are referencing the prime numbers by way of the [ordinal numbers](https://en.wikipedia.org/wiki/Ordinal_number).  
  
  We could, at this point, get caught in a trap and say, "Well, since 2 is the first prime and 1 = *e*, shouldn't 2 = *e*-*e*. And what happens when we get to the fourth prime, should it be called the (2-2)th prime, which should then be the ((e-e)-(e-e))th prime???""  At that point we would be right back where we started from with simply counting *e*'s.  We avoid this trap by saying that the novelties are ordered according to the elements of *e*.  Since we fully understand *e* as all the bundles of ones, we can make perfect sense of the number 10 as ten bundles of one (or as the 10th member of e).  Effectively, I am arguing that the ordinal numbers are immutable with respect to their representation, and so we will adopt a representation of them that is familiar; the base 10 number system.

  There is no real reason to do any of this, but I found it very interesting to think of a world in which the basic understanding of quantities was described multiplicatively instead of additively. In such a world, prime numbers would truly be considered the building blocks of numeracy, going so far as to say composite numbers don't even exist as unique entities. As another point of interest, the Novelties are an example of a non-positional numbering system where multiplication and division are trivial, while addition and subtraction are very hard.
