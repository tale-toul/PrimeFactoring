#!/usr/bin/env python
'''This is version 1.0.0 of the factorization of integer numbers.
It is simple but very inneficient, the factorization of a prime number 
like 45834473 takes more than 14 seconds
'''
#Test number 7102454841, takes about 1minute and 21 seconds

#Version 1.0.2

import sys
import time

#Number to factor
num=0;
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


#####MAIN#######

if(len(sys.argv)>1):
    try:
        num=int(sys.argv[1])
    except:
        print "Could not convert",sys.argv[1], "into an integer"
        print "Usage:",sys.argv[0], "<positive integer>"
        exit(-1)
    t_start=time.time()
    factors=factorize(num)
    t_end=time.time()
    if validate_factors(int(sys.argv[1]),factors):
        print "Factors of",sys.argv[1],"=",factors,"In",t_end-t_start,"seconds"
        exit(0)
    else:
        print "The result is wrong, multiplying",factors,"doesn't yield",sys.argv[1]
        exit(-2)
else:
    print "Usage:",sys.argv[0], "<positive integer>"
