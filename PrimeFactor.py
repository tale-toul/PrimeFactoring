#!/usr/bin/env python

#Version 1.2.0

import sys
import time
import argparse
import os.path
import json
import signal
import inspect
#import pdb

factors=[] #List of found factors of number

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
    signal.signal(signal.SIGUSR1,signal_show_current_status) #Sets the handler for the signal SIGUSR1
    try:
        while candidate == 2: #Consider 2 as a special case
            if(compnum%candidate == 0):
                pfactors.append(candidate)
                compnum /= candidate
            else:
                candidate += 1 #Now candidate equals 3
        while candidate == 3: #Consider 3 as a special case
            if(compnum%candidate == 0):
                pfactors.append(candidate)
                compnum /= candidate
            else:
                candidate += 2 #Now candidate equals 5
        while candidate == 5: #Consider 5 as a special case
            if(compnum%candidate == 0):
                pfactors.append(candidate)
                compnum /= candidate
            else:
                candidate += 2 #Now candidate equals 7
        while candidate <= compnum: #Bucle general
            while compnum%candidate == 0: # For candidates ending in 7
                pfactors.append(candidate)
                compnum /= candidate
            candidate += 2 #Only check for odd numbers, even numbers cannot be primes
            while compnum%candidate == 0: #For candidates ending in 9
                pfactors.append(candidate)
                compnum /= candidate
            candidate += 2
            while compnum%candidate == 0: #For candidates ending in 1
                pfactors.append(candidate)
                compnum /= candidate
            candidate += 2
            while compnum%candidate == 0: #For candidates ending in 3
                pfactors.append(candidate)
                compnum /= candidate
            candidate += 4
        signal.signal(signal.SIGUSR1,signal.SIG_DFL) #Sets the handler to its default state
        return pfactors #In the end at least pfactors contains compnum
    except KeyboardInterrupt:
        print "Program interrupted by user"
        print "Factors found so far:",pfactors
        print "Last candidate:",candidate
        raise

#Parameters: none
#Return value: the arguments found in the command line
#Parses the command line arguments
def parse_arguments():
    parser=argparse.ArgumentParser(description="Find the prime factors of an integer number")
    disjunt=parser.add_mutually_exclusive_group()
    #Next one is actually optional, just in case we are running the test batch
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
    global t_start
    test_cases=read_test_cases(batch_file) #Load or create a dictionary of test cases
    count=1
    test_cases_size=len(test_cases)
    if test_cases_size >0: #There are tests to be run
        Ky=test_cases.keys() #Get a list of the keys (numbers) in the dictionary
        Ky.sort(key=int) #sort the list numerically
        for case in Ky: #case is a string
            if arguments.verbose: print case
            t_start=time.time()
            factors=factorize(int(case))
            t_end=time.time()
            if factors == test_cases[case] and arguments.verbose: 
                print "\t",factors, "Passed in",round(t_end-t_start,4),"seconds.", count,"of", test_cases_size
            elif factors != test_cases[case]:
                print "FAILED test:", case,test_cases[case],"!=",case,factors,"time",round(t_end-t_start,4),"seconds"
                raw_input("Press any key to continue")
            count +=1
    else: print "Empty test case batch"

#Parameters: signum.- The signal number used with this function
#           stack.- The current stack frame 
#Return value.- Nothing is returned
#This function is called automatically when the captured signal is received.  After the
#execution of this function the program should continue running where it was before the
#signal was catched.
#We never call this function, it is called by the signal handler
def signal_show_current_status(signum,stack):
   (args,varargs,keywords,local_vars)=inspect.getargvalues(stack)
   print "Received signal",signum
   print "\tFactors found so far:",local_vars['pfactors']
   print "\tLast candidate:",local_vars['candidate']
   t_so_far=time.time()
   print "\tTime used:", round(t_so_far-t_start,3),"seconds"


#####MAIN#######

#pdb.set_trace()  #Uncomment to debug

arguments=parse_arguments()
if arguments.num < 1:
    print "The number to factor must be a positive integer"
    exit(-4)
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
try:
    factors=factorize(arguments.num)
except KeyboardInterrupt:
    t_end=time.time()
    print "Time used",round(t_end-t_start,4),"seconds"
    exit(3)
t_end=time.time()

if len(factors)== 1 or validate_factors(arguments.num,factors): #If there's only one factor or they multiply to the orignal number
    print "Factors of",arguments.num,"=",factors,
    if arguments.verbose: print "In",round(t_end-t_start,4),"seconds"
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
