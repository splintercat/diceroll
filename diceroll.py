import math
import argparse
import sys
from fractions import Fraction
## calculate the cumulative binomial distribution
## basically calculate odds of success given a dice pool size in shadowrun

def floatStr(s):
  try:
    n = float(Fraction(s))
  except:
    raise argparse.ArgumentTypeError("%s is not a float"%(s,))
  if n < 0.0 or n > 1.0:
    raise argparse.ArgumentTypeError("%s is negative or greater than 1"%(s,))
  return n


parser = argparse.ArgumentParser(description="calculate the odds of success for a dice roll")

parser.add_argument('-d', '--dice', type=int, help="number of dice to roll")
parser.add_argument('-n', '--hits', type=int, help='minimum number of successes/hits')
group = parser.add_mutually_exclusive_group(required=True)
group.add_argument('-s', '--sr', action='store_true', help='use shadorun dice for probability (2.0/6.0)')
group.add_argument('-p', '--prob', type=floatStr, default=0, help='probability of success for a given die roll.  Please enter the number between 0 and 1. Entries like .4 and 1/3 are both accepted')


def sigma(func, i, k):
  """ take a function that accepts one input
  and iterates from i to k summing the results
  a.k.a sigma notation
  """
  result=0
  for x in range(i, k+1):
    result+=func(x)
  return result

def pmf(k,n,p):
  """probability math function
  n choose k
  n = number of observations
  k = desired successes
  p = probability
  example: 4 coin flips, 2 are heads
  """
  return (math.factorial(n)/(math.factorial(k)*math.factorial(n - k)))*(p**k)*(1 - p)**(n - k)

def cds(k,n,p):
  """ cumulative distribution of success
  k = minimum desired successes
  n = number of observation (aka number of rolled dice)
  p = probability of success
  """
  result = []
  for x in range(k,n+1):
    result.append(pmf(x,n,p))
  return math.fsum(result)

args =	vars(parser.parse_args())
print(str(args))
probability = 0
hits = args['hits']
dice = args['dice']
if (args['sr'] == True):
  probability = 1.0/3.0
else:
  probability = args['prob']

if probability == 0:
  print("probability appears to be zero, exiting")
  sys.exit(1) 

print("Chance of getting at least " + str(hits) + ":" )
print(str(cds(hits, dice, probability))) 
