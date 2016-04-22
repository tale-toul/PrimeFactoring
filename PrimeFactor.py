#!/usr/bin/env python

#Version 1.3.6

import sys
import time
import argparse
import os.path
import json
import signal
import inspect
import math
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
#           candidate.- The first candidate to start looking for factors
#Return value.- the list of factors
#The core functionality of program, finds the prime factors of compnum
def factorize(compnum,candidate=2):
    increments_dict={'7':[2,2,2,4],
                     '9':[2,2,4,2],
                     '1':[2,4,2,2],
                     '3':[4,2,2,2]}
    increment=increments_dict['7'] #By default the 7 increment list is used
    max_candidate=int(math.ceil(math.sqrt(compnum))) #Square root of the number to factor
    pfactors=[] #List of found factors 
    if candidate > 5:
        text_candidate_last=str(candidate)[-1]
#Place the candidate in the correct position; if the candidate ends in 7, 9, 1 or 3 do nothing
        if text_candidate_last == '4' or text_candidate_last == '5' or text_candidate_last == '6':
            text_candidate_last='7' #Bring it up to next number ending in 7
        elif text_candidate_last == '8':
            text_candidate_last='9' #Bring it up to next number ending in 9
        elif text_candidate_last == '0':
            text_candidate_last='1' #Bring it up to next number ending in 1
        elif text_candidate_last == '2':
            text_candidate_last='3' #Bring it up to next number ending in 3
        candidate =int(str(candidate)[:-1]+text_candidate_last) #Add the new ending 
#Now use the correct increment list
        increment=increments_dict[text_candidate_last]
    signal.signal(signal.SIGUSR1,signal_show_current_status) #Sets the handler for the signal SIGUSR1
    try:
        if candidate == 2: #This condition is here because the initial value of candidate may be different from 2
            while compnum%candidate == 0:  #Candidate = 2, consider it as a special case
                pfactors.append(candidate)
                compnum /= candidate
                max_candidate =int(math.ceil(math.sqrt(compnum))) #Square root of the number to factor
            candidate += 1 #Now candidate equals 3
        if candidate == 3: #This condition is here because the initial value of candidate may be different from 2
            while compnum%candidate == 0: 
                pfactors.append(candidate)
                compnum /= candidate
                max_candidate = int(math.ceil(math.sqrt(compnum))) #Square root of the number to factor
            candidate += 2 #Now candidate equals 5
        if candidate ==4: candidate =5 #Upgrade to the next meaninful candidate
        if candidate == 5: #This condition is here because the initial value of candidate may be different from 2
            while compnum%candidate == 0: 
                pfactors.append(candidate)
                compnum /= candidate
                max_candidate = int(math.ceil(math.sqrt(compnum))) #Square root of the number to factor
            candidate += 2 #Now candidate equals 7
#----MAIN LOOP----
        while candidate <= max_candidate: 
            while compnum%candidate == 0: # For candidates ending in 7
                pfactors.append(candidate)
                compnum /= candidate
                max_candidate = int(math.ceil(math.sqrt(compnum))) #Square root of the number to factor
            candidate += increment[0] #This increment depends on the incremnet list selected bejore
            while compnum%candidate == 0: #For candidates ending in 9
                pfactors.append(candidate)
                compnum /= candidate
                max_candidate = int(math.ceil(math.sqrt(compnum))) #Square root of the number to factor
            candidate += increment[1] #This increment depends on the incremnet list selected bejore
            while compnum%candidate == 0: #For candidates ending in 1
                pfactors.append(candidate)
                compnum /= candidate
                max_candidate = int(math.ceil(math.sqrt(compnum))) #Square root of the number to factor
            candidate += increment[2] #This increment depends on the incremnet list selected bejore
            while compnum%candidate == 0: #For candidates ending in 3
                pfactors.append(candidate)
                compnum /= candidate
                max_candidate = int(math.ceil(math.sqrt(compnum))) #Square root of the number to factor
            candidate += increment[3] #This increment depends on the incremnet list selected bejore
        if compnum != 1: pfactors.append(compnum) 
        signal.signal(signal.SIGUSR1,signal.SIG_DFL) #Sets the handler to its default state
        return pfactors #In the end at least pfactors contains compnum
    except KeyboardInterrupt:
        print "Program interrupted by user"
        print "Factors found so far:",pfactors
        print "Last candidate:",candidate
        raise



#Parameters: num.- An integer to factorize
#           first_candidate.- The first candidate to start looking for factors
#           last_candidate.- The last candidate to try
#Return value.- the list of factors
#The core functionality of program, finds the prime factors of compnum
def factorize_with_limits(compnum,candidate=2,last_candidate=2):
    increments_dict={'7':[2,2,2,4],
                     '9':[2,2,4,2],
                     '1':[2,4,2,2],
                     '3':[4,2,2,2]}
    increment=increments_dict['7'] #By default the 7 increment list is used
    max_candidate=min(last_candidate,int(math.ceil(math.sqrt(compnum)))) #Square root of the number to factor
    pfactors=[] #List of found factors 
    if candidate > 5:
        text_candidate_last=str(candidate)[-1]
#Place the candidate in the correct position; if the candidate ends in 7, 9, 1 or 3 do nothing
        if text_candidate_last == '4' or text_candidate_last == '5' or text_candidate_last == '6':
            text_candidate_last='7' #Bring it up to next number ending in 7
        elif text_candidate_last == '8':
            text_candidate_last='9' #Bring it up to next number ending in 9
        elif text_candidate_last == '0':
            text_candidate_last='1' #Bring it up to next number ending in 1
        elif text_candidate_last == '2':
            text_candidate_last='3' #Bring it up to next number ending in 3
        candidate =int(str(candidate)[:-1]+text_candidate_last) #Add the new ending 
#Now use the correct increment list
        increment=increments_dict[text_candidate_last]
    signal.signal(signal.SIGUSR1,signal_show_current_status) #Sets the handler for the signal SIGUSR1
    try:
        if candidate == 2: #This condition is here because the initial value of candidate may be different from 2
            while compnum%candidate == 0:  #Candidate = 2, consider it as a special case
                pfactors.append(candidate)
                compnum /= candidate
                max_candidate=min(last_candidate,int(math.ceil(math.sqrt(compnum)))) #Square root of the number to factor
            candidate += 1 #Now candidate equals 3
        if candidate == 3: #This condition is here because the initial value of candidate may be different from 2
            while compnum%candidate == 0: 
                pfactors.append(candidate)
                compnum /= candidate
                max_candidate=min(last_candidate,int(math.ceil(math.sqrt(compnum)))) #Square root of the number to factor
            candidate += 2 #Now candidate equals 5
        if candidate ==4: candidate =5 #Upgrade to the next meaninful candidate
        if candidate == 5: #This condition is here because the initial value of candidate may be different from 2
            while compnum%candidate == 0: 
                pfactors.append(candidate)
                compnum /= candidate
                max_candidate=min(last_candidate,int(math.ceil(math.sqrt(compnum)))) #Square root of the number to factor
            candidate += 2 #Now candidate equals 7
#----MAIN LOOP----
        while candidate <= max_candidate: 
            while compnum%candidate == 0: # For candidates ending in 7
                pfactors.append(candidate)
                compnum /= candidate
                max_candidate=min(last_candidate,int(math.ceil(math.sqrt(compnum)))) #Square root of the number to factor
            candidate += increment[0] #This increment depends on the incremnet list selected bejore
            while compnum%candidate == 0: #For candidates ending in 9
                pfactors.append(candidate)
                compnum /= candidate
                max_candidate=min(last_candidate,int(math.ceil(math.sqrt(compnum)))) #Square root of the number to factor
            candidate += increment[1] #This increment depends on the incremnet list selected bejore
            while compnum%candidate == 0: #For candidates ending in 1
                pfactors.append(candidate)
                compnum /= candidate
                max_candidate=min(last_candidate,int(math.ceil(math.sqrt(compnum)))) #Square root of the number to factor
            candidate += increment[2] #This increment depends on the incremnet list selected bejore
            while compnum%candidate == 0: #For candidates ending in 3
                pfactors.append(candidate)
                compnum /= candidate
                max_candidate=min(last_candidate,int(math.ceil(math.sqrt(compnum)))) #Square root of the number to factor
            candidate += increment[3] #This increment depends on the incremnet list selected bejore
        if compnum != 1: pfactors.append(compnum) 
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
    parser.add_argument("-c", "--firstcandi", help="First candidate to start factoring the number", type=int)
    parser.add_argument("-l", "--lastcandi", help="Last candidate to check for primes", type=int)
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
    count=1 #The case number I'm about to try
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
if arguments.firstcandi is not None:#An initial candidate has been assigned via the command line 
    if arguments.firstcandi >= 2:
        candidate=arguments.firstcandi
    else:
        print "The first posible candidate must be at least 2, you have entered",arguments.firstcandi 
        exit(-5)
else: arguments.firstcandi = 2 #Default value
if arguments.lastcandi is not None: #A last candidate has been assigned via the command line
    if arguments.lastcandi >= 2:
        last_candidate=arguments.lastcandi
    else:
        print "The last posible andidate must be at least 2, you have entered",arguments.lastcandi
        exit(-6)
else: arguments.lastcandi = arguments.num
if arguments.runtest: #If running the test cases
    run_test_cases(arguments.runtest)
else: #Not running tests
    if arguments.addtest:#Save the test case if requested and it has not been saved before
        test_cases=read_test_cases(arguments.addtest) #Load or create a dictionary of test cases
        if str(arguments.num) in test_cases: #If the test case already exists, say so and exit
            print "Test case",arguments.num,"already present:",arguments.num,"=",test_cases[str(arguments.num)]
            exit(2)
    t_start=time.time()
    try:
        factors=factorize_with_limits(arguments.num,arguments.firstcandi,arguments.lastcandi)
    except KeyboardInterrupt:
        t_end=time.time()
        print "Time used",round(t_end-t_start,4),"seconds"
        exit(3)
    t_end=time.time()

    if len(factors)== 1 or validate_factors(arguments.num,factors): #If there's only one factor or they multiply to the orignal number
        print "Factors of",arguments.num,"=",factors,
        if arguments.verbose: print "In",round(t_end-t_start,4),"seconds"
        if arguments.addtest:#Save the test case 
            test_cases[arguments.num]=factors
            try:
                f_out=open(arguments.addtest,"w")
            except:
                print "Could not open file",arguments.addtest,"to write"
                f_out.close()
                exit(-3)
            f_out.write(json.dumps(test_cases))
            f_out.close()
        exit(0)
    else:
        print "The result is wrong, multiplying",factors,"doesn't yield",arguments.num
        exit(-1)
