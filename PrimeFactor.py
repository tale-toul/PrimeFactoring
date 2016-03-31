#!/usr/bin/env python
'''This is version 1.0.0 of the factorization of integer numbers.
It is simple but very inneficient, the factorization of a prime number 
like 45834473 takes more than 14 seconds
'''
#Test number 7102454841, takes about 1minute and 21 seconds

#Version 1.0.4

import sys
import time
import argparse
import os.path
import json

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
    parser.add_argument("--addtest",  help="Adds the results of factoring this number, as a test case, to the file specified")
    return(parser.parse_args()) 

#Parameters: The file to read the test cases from
#Return: the dictionary containing the test cases
#Tries to read a file containing the json serialized dictionary containing the test
#cases.  If the file doesn't exists returns an empty dictionary
def read_test_cases(file):
    test_cases_dict=dict()
    if os.path.isfile(file): #If file exists, load it
        try:
            f_in=open(file)
        except:
            print "Could not open file",file,"to read"
            exit(-2)
        test_serialized=f_in.read()
        test_cases_dict=json.loads(test_serialized)
        f_in.close()
    return test_cases_dict #If file doesn't exist return an empty dictionary





#####MAIN#######

arguments=parse_arguments()
if arguments.addtest: test_cases=read_test_cases(arguments.addtest) #Load or create a dictionary of test cases
t_start=time.time()
factors=factorize(arguments.num)
t_end=time.time()
if validate_factors(arguments.num,factors):
    print "Factors of",arguments.num,"=",factors,
    if arguments.verbose: print "In",t_end-t_start,"seconds"
    if arguments.addtest and arguments.num not in test_cases:#Save the test case if requested and it has not been saved before
        test_cases[arguments.num]=factors
        try:
            f_out=open(arguments.addtest,"w")
        except:
            print "Could not open file",arguments.addtest,"to write"
            exit(-3)
        f_out.write(json.dumps(test_cases))
        f_out.close()
    exit(0)
else:
    print "The result is wrong, multiplying",factors,"doesn't yield",arguments.num
    exit(-1)
