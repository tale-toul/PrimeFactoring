#!/usr/bin/env python
'''This is version 1.0.0 of the factorization of integer numbers.
It is simple but very inneficient, the factorization of a prime number 
like 45834473 takes more than 14 seconds
'''
#Test number 7102454841, takes about 1minute and 21 seconds

#Version 1.0.1

import sys

#Number to factor
num=0;
#Candidate to be a factor of num
candidate=2
#List of factors
factors=[]

#Parameters: num.- An integer 
#            factors.- A list of integers
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



#####MAIN#######

if(len(sys.argv)>1):
    try:
        num=int(sys.argv[1])
    except:
        print "Could not convert",sys.argv[1], "into an integer"
        print "Usage:",sys.argv[0], "<positive integer>"
        exit(-1)
    while(candidate <= num):
        if(num%candidate == 0):
            factors.append(candidate)
            num /= candidate
        else:
            candidate +=1
    if validate_factors(int(sys.argv[1]),factors):
        print "Factors of",sys.argv[1],"=",factors
        exit(0)
    else:
        print "The result is wrong, multiplying",factors,"doesn't yield",sys.argv[1]
        exit(-2)
else:
    print "Usage:",sys.argv[0], "<positive integer>"
