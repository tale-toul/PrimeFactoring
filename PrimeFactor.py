#!/usr/bin/env python
'''This is version 1.0.0 of the factorization of integer numbers.
It is simple but very inneficient, the factorization of a prime number 
like 45834473 takes more than 14 seconds
'''
#Test number 7102454841, takes about 1minute and 21 seconds

#Version 1.0.7

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

    try:
        while(candidate <= compnum):
            if(compnum%candidate == 0):
                pfactors.append(candidate)
                compnum /= candidate
            else:
                candidate +=1
        return pfactors #In the end at least pfactors contains compnum
    except KeyboardInterrupt:
        print "Program interrupted by user"
        print "Factors found so far:",pfactors
        print "Last candidate:",candidate
        exit(3)

#Parameters: none
#Return value: the arguments found in the command line
#Parses the command line arguments
def parse_arguments():
    parser=argparse.ArgumentParser(description="Find the prime factors of an integer number")
    disjunt=parser.add_mutually_exclusive_group()
    #Next one is actually optional, in case we are running the test batch
    parser.add_argument("num", nargs="?", default=1, help="Integer number to factor", type=int)
    parser.add_argument("-v", "--verbose", help="Verbose output", action="store_true")
    disjunt.add_argument("--addtest", metavar="FILE",  help="Adds the results of factoring this number, as a test case, to the file specified")
    disjunt.add_argument("--runtest", metavar="FILE", help="Run the test cases")
    return(parser.parse_args()) 

#Parameters: The file to read the test cases from
#Return: the dictionary containing the test cases
#Tries to read a file containing the json serialized dictionary containing the test
#cases and load them into a dictionary.  If the file doesn't exists returns an empty dictionary
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

#Parameters: The file to read the test cases from
#Return: void
#Factorizes the numbers stored as test cases and compares the results with the ones found
#in the test cases
def run_test_cases(batch_file):
    test_cases=read_test_cases(batch_file) #Load or create a dictionary of test cases
    if len(test_cases) >0: #There are tests to be run
        if arguments.verbose: print "Running",len(test_cases),"test cases"
        for case in test_cases: #case is a string
            if arguments.verbose: print case,
            t_start=time.time()
            factors=factorize(int(case))
            t_end=time.time()
            if factors == test_cases[case] and arguments.verbose: print factors, "Passed in",t_end-t_start,"seconds"
            elif factors != test_cases[case]:
                print "FAILED test:", case,test_cases[case],"!=",case,factors,"time",t_end-t_start,"seconds"
    else: print "Empty test case batch"




#####MAIN#######

arguments=parse_arguments()
if arguments.addtest:#If we are adding a new test case 
    test_cases=read_test_cases(arguments.addtest) #Load or create a dictionary of test cases
    if str(arguments.num) in test_cases: #If the test case already exists, say so and exit
        print "Test case",arguments.num,"already present:",arguments.num,"=",test_cases[str(arguments.num)]
        exit(2)
elif arguments.runtest: #If running the test cases
    run_test_cases(arguments.runtest)
    exit(1) #If we are running test the program ends here
#Not running test, so we continue 
t_start=time.time()
factors=factorize(arguments.num)
t_end=time.time()
if validate_factors(arguments.num,factors):
    print "Factors of",arguments.num,"=",factors,
    if arguments.verbose: print "In",t_end-t_start,"seconds"
    if arguments.addtest:#Save the test case if requested and it has not been saved before
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
