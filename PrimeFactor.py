#!/usr/bin/env python
'''This is version 1.0.0 of the factorization of integer numbers.
It is simple but very inneficient, the factorization of a prime number 
like 45834473 takes more than 14 seconds
'''
#Test number 7102454841, takes about 1minute and 21 seconds
import sys

#Number to factor
num=0;
#Candidate to be a factor of num
candidate=2
#List of factors
factors=[]

if(len(sys.argv)>1):
    try:
        num=int(sys.argv[1])
    except:
        print "Could not convert",sys.argv[1], "into an integer"
        exit(1)
    while(candidate <= num):
        if(num%candidate == 0):
            factors.append(candidate)
            num /= candidate
        else:
            candidate +=1
    print "Factors of",sys.argv[1],"=",factors
else:
    print "Usage:",sys.argv[0], "<positive integer>"
