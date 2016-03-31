#!/usr/bin/env python
'''This is version 1.0.0 of the factorization of integer numbers.
It is simple but very inneficient, the factorization of a prime number 
like 45834473 takes more than 14 seconds
'''
#Test number 7102454841, takes about 1minute and 21 seconds

#Version 1.0.3

import sys
import time
import argparse

#List of factors
factors=[]

#Parameters: num.- An integer 
#            factors.- A list of integers
#Return value.- True if the result of the multiplication yields the num, False otherwise
#The function checks that multiplying the factors in the list factors renders the value
#stored in the variable num
def validate_factors(num,factors):
    partial_result=1
    for items in factors:
        partial_result *= items
    if partial_result == num:
        return True
    else:
        return False

#Parameters: num.- An integer to factorize
#Return value.- the list of factors
#The core functionality of program, finds the prime factors of compnum
def factorize(compnum):
    candidate=2 #Candidate to be a factor of num
    pfactors=[] #List of found factors of number

    while(candidate <= compnum):
        if(compnum%candidate == 0):
            pfactors.append(candidate)
            compnum /= candidate
        else:
            candidate +=1
    return pfactors #In the end at least pfactors contains compnum

#Parameters: none
#Return value: the arguments found in the command line
#Parses the command line arguments
def parse_arguments():
    parser=argparse.ArgumentParser(description="Find the prime factors of an integer number")
    parser.add_argument("num", help="Integer number to factor", type=int)
    parser.add_argument("-v", "--verbose", help="Verbose output", action="store_true")
    return(parser.parse_args())


#####MAIN#######

arguments=parse_arguments()
t_start=time.time()
factors=factorize(arguments.num)
t_end=time.time()
if validate_factors(arguments.num,factors):
    print "Factors of",sys.argv[1],"=",factors,
    if arguments.verbose: print "In",t_end-t_start,"seconds"
    exit(0)
else:
    print "The result is wrong, multiplying",factors,"doesn't yield",arguments.num
    exit(-1)
