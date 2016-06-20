#!/usr/bin/env python

#Version 2.4.3

import sys
import time
import argparse
import os, os.path
import json
import signal
import inspect
import math,random
import multiprocessing
from multiprocessing import Process,Manager,Lock,Event,Condition,Queue
import gmpy2
import NetCodePrimeF

#import pdb

factors=list() #List of number's found factors

#Parameters: num.- An integer 
#            factors.- A list of integers
#Return value.- True if the result of the multiplication yields the num, False otherwise
#The function checks that multiplying the factors in the list factors renders the value
#stored in the variable num
def validate_factors(num,factors):
    '''Checks that the factors are possibly prime, and that its product yields the number'''
    partial_result=1
    for item in factors:
        if gmpy2.is_prime(item):
            partial_result *= item
        else:
            print "%d is not prime" % (item,)
            return False
    return True if partial_result == num else False # Ternary expression

#Parameters: compnum.- An integer to factorize
#            own_results.- list to store the factors found during the execution of the
#                       function.  Belongs to a multiprocessing Manager so it's visible
#                       outside the process
#           candidate.- The first candidate to start looking for factors
#           last_candidate.- The last candidate to try
#           max_candidate.- The maximun value a candidate can get to look for factors
#           phase1.- Are we running in phase1 mode, if not leave as soon as we find a
#Returns: The updated values of compnum and max_candidate. The own_results is also
#         updated, but this is done in-place
def update_resnum(compnum,own_results,candidate,last_candidate,max_candidate,phase1):
    '''This function is called when a new factor is found. Adds the factor found to the
    results list; updates the number to factor, dividing it by the factor found; and
    updates the maximun candidate, making it -1 in case we are NOT in phase 1, what causes
    and inmediate exit of the factoring process '''
    own_results.append(candidate)
    compnum /= candidate
    if not phase1:
        max_candidate=-1 # Return ASAP
    else:
        max_candidate=min(last_candidate,int(math.ceil(math.sqrt(compnum)))) #Square root of the number to factor
    return (compnum,max_candidate)

#Parameters: compnum.- An integer to factorize
#           own_results.- list to store the factors found during the execution of the
#             function.  Belongs to a multiprocessing Manager so it's visible outside the
#             process
#           nms.- multiprocessing Namespace to share variables with the outside processes.
#           loc.- multiprocessing Lock to controll access to own_results
#           event.- An event object to use along with signal to control the passing of
#               info to the factorize broker, before dying
#           cond.- multiprocessing condition used to signal the parent process that this
#               process has finished
#           candidate.- The first candidate to start looking for factors
#           last_candidate.- The last candidate to try
#           phase1.- Are we running in phase1 mode, if not leave as soon as we find a
#                    factor
#Return:  The list of factors found, with duplacates, it needs cleaning
def factorize_with_limits(compnum,own_results,nms,loc,event,cond,candidate=2,last_candidate=2,
                          phase1=False):
    '''The core functionality of the program.  Multiprocess function used to factor a
    number, it will look for factors inside a defined segment, between an initial and a
    final possible candidates. All factors found are saved and returned to the parent
    process'''

    #This data structure is used to adjust the initial candidate, and select the correct
    #increment dictionary 
    cand_adj_increments= {0:('1',[2,4,2,2]),
                          1:('1',[2,4,2,2]),
                          2:('3',[4,2,2,2]),
                          3:('3',[4,2,2,2]),
                          4:('7',[2,2,2,4]),
                          5:('7',[2,2,2,4]),
                          6:('7',[2,2,2,4]),
                          7:('7',[2,2,2,4]),
                          8:('9',[2,2,4,2]),
                          9:('9',[2,2,4,2])}
                     
    max_candidate=min(last_candidate,int(math.ceil(math.sqrt(compnum)))) #Square root of the number to factor
#Place the candidate in the correct position; if the candidate ends in 7, 9, 1 or 3 do nothing
    if candidate > 5:
        updated_last_figure ,increment = cand_adj_increments[candidate%10]
        candidate =int(str(candidate)[:-1]+updated_last_figure) #Add the new ending 
    else: #candidate is 2, 3, 4 or 5
        increment=cand_adj_increments[7][1] #The 7 increment list is used

    signal.signal(signal.SIGUSR1,signal_show_current_status) #Sets the handler for the signal SIGUSR1
    if candidate == 2: #This condition is here because the initial value of candidate may be different from 2
        while compnum%candidate == 0:  #Candidate = 2, consider it as a special case
            loc.acquire()
            compnum,max_candidate=update_resnum(compnum,own_results,candidate,last_candidate,max_candidate,phase1)
            loc.release()
        candidate += 1 #Now candidate equals 3
    if candidate == 3: #This condition is here because the initial value of candidate may be different from 2
        while compnum%candidate == 0:
            loc.acquire()
            compnum,max_candidate=update_resnum(compnum,own_results,candidate,last_candidate,max_candidate,phase1)
            loc.release()
        candidate += 2 #Now candidate equals 5
    if candidate == 4: candidate = 5 #Upgrade to the next meaninful candidate
    if candidate == 5: #This condition is here because the initial value of candidate may be different from 2
        while compnum%candidate == 0:
            loc.acquire()
            compnum,max_candidate=update_resnum(compnum,own_results,candidate,last_candidate,max_candidate,phase1)
            loc.release()
        candidate += 2 #Now candidate equals 7
#----MAIN LOOP----
    while candidate <= max_candidate:
        while compnum%candidate == 0: 
            loc.acquire()
            compnum,max_candidate=update_resnum(compnum,own_results,candidate,last_candidate,max_candidate,phase1)
            loc.release()
        candidate += increment[0] #This increment depends on the incremnet list selected bejore
        while compnum%candidate == 0: 
            loc.acquire()
            compnum,max_candidate=update_resnum(compnum,own_results,candidate,last_candidate,max_candidate,phase1)
            loc.release()
        candidate += increment[1] #This increment depends on the incremnet list selected bejore
        while compnum%candidate == 0: 
            loc.acquire()
            compnum,max_candidate=update_resnum(compnum,own_results,candidate,last_candidate,max_candidate,phase1)
            loc.release()
        candidate += increment[2] #This increment depends on the incremnet list selected bejore
        while compnum%candidate == 0: 
            loc.acquire()
            compnum,max_candidate=update_resnum(compnum,own_results,candidate,last_candidate,max_candidate,phase1)
            loc.release()
        candidate += increment[3] #This increment depends on the incremnet list selected bejore
    loc.acquire()
    if compnum != 1: own_results.append(compnum)
    loc.release()
    cond.acquire()
    nms.end_of_process=True
    cond.notify()
    cond.release()


#Parameters: compnum.- number to factor
#           possible_factors.- a list of posible factors to try
#Returns:   a list of the found factors within the set provided, hopefully only the prime
#           factors. The last element of the list is the compnum itself
def factorize_with_factors(compnum,possible_factors):
    '''Since there is no need to actually look for candidate the funcion is a lot simpler'''
    max_candidate=int(math.ceil(math.sqrt(compnum))) 
    pfactors=[] #List of found factors
    #Remove duplicates and order the list in reverse order
    order_uniq_pfactors=list(set(possible_factors))
    order_uniq_pfactors.sort(key=int,reverse=True)
    candidate=order_uniq_pfactors.pop()
    while candidate <= max_candidate:
        while compnum%candidate == 0: 
            pfactors.append(candidate)
            compnum /= candidate
            max_candidate = int(math.ceil(math.sqrt(compnum))) 
        if order_uniq_pfactors:
            candidate=order_uniq_pfactors.pop() #I'm not checking that the list is empty
    if compnum != 1: pfactors.append(compnum)
    return pfactors #In the end at least pfactors contains compnum



#Parameters: none
#Return value: the arguments found in the command line
def parse_arguments():
    '''Parses the command line arguments'''
    parser=argparse.ArgumentParser(description="Find the prime factors of an integer number")
    disjunt=parser.add_mutually_exclusive_group()
    #Next one is actually optional, just in case we are running the test batch
    parser.add_argument("num", nargs="?", default=1, help="Integer number to factor", type=int)
    parser.add_argument("-v", "--verbose", help="Verbose output", action="store_true")
    parser.add_argument("-c", "--firstcandi", help="First candidate to start factoring the number", type=int)
    parser.add_argument("-l", "--lastcandi", help="Last candidate to check for primes", type=int)
    disjunt.add_argument("--addtest", metavar="FILE",  help="Adds the results of factoring this number, as a test case, to the file specified")
    disjunt.add_argument("--runtest", metavar="FILE", help="Run the test cases")
    return parser.parse_args()

#Parameters: The file to read the test cases from
#Return: the dictionary containing the test cases
def read_test_cases(file):
    '''Tries to read a file containing the json serialized dictionary with the test cases
    and load them into a dictionary.  If the file doesn't exists returns an empty
    dictionary'''
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
def run_test_cases(batch_file):
    '''Factors the numbers stored as test cases and compares the results with the ones
    found in the test cases'''
    global t_start
    test_cases=read_test_cases(batch_file) #Load or create a dictionary of test cases
    count=1 #The case number I'm about to try
    test_cases_size=len(test_cases)
    if test_cases_size > 0: #There are tests to be run
        Ky=test_cases.keys() #Get a list of the keys (numbers) in the dictionary
        Ky.sort(key=int) #sort the list numerically
        for case in Ky: #case is a string
            if arguments.verbose: print case
            t_start=time.time()
            factors=factor_broker(int(case),2,int(case))
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
   print "Received signal %d" % signum
   #print "local_vars:",local_vars #Dump the local_vars dictionary
   local_vars['own_results'].append(local_vars['compnum'])
   print "\tFactors found so far: %s"%local_vars['own_results']
   print "\tLast candidate tried: %d"%local_vars['candidate']
   local_vars['nms'].last_candidate=local_vars['candidate']
   local_vars['nms'].compnum=local_vars['compnum']
   t_so_far=time.time()
   print "\tTime used: %.2f" % round(t_so_far-t_start,3),"seconds"
   local_vars['event'].set()


#Parameters: results_to_clean.- list of lists with the results returned by the factoring
#                               of the different segments
#           num_to_factor.- The number to factor, is needed as a reference to clean up the
#           factors
#Return value: the list of prime factors with respect to this results
def clean_results(results_to_clean,num_to_factor):
    '''Removes the composite numbers and leaves only the prime numbers from the result
    set given.'''
    # This is a list comprehension that flattens the list of lists that is # results_to_clean
    wfactors=[ffactor for result_tranche in results_to_clean 
                            for ffactor in result_tranche]
    return factorize_with_factors(num_to_factor,wfactors) if wfactors else [num_to_factor]


#Parameters: num_to_factor.- The number to factor
#            bottom.-First number of the set to start looking for factors
#            top.- Last number of the set to look for factors
def factor_broker(num_to_factor,bottom,top):
    '''Divides the factoring problem in many equal segments.  Calls the factorize function
    for the smaller problems'''
    segments=list() #The list of segments to divide the problem into
    pending_remote_segments=list()
    list_of_nums_to_factor=[num_to_factor] #The list of pending components of the number to factor
    orig_num_to_factor=num_to_factor #The original num_to_factor
    manager=Manager() #To access common elements among processes
    cond_loc=Lock()
    cond=Condition(cond_loc)
    factor_eng=list() #This is a complex data structure used to keep information across
    #the processes.  Each element in the list represents a factoring process and it's
    #made of the following elements:
    #[0].-own_results.- a multiprocessing shared list to store the found factors by the
    #       process in the segment
    #[1].-job.- the handler to the process itself
    #[2].-nms.- a multiprocessing shared namespace used to return variables from the
    #       processes.
    #[3].-loc.- a multiprocessing Lock to control de update of the own_results list, the
    #       number to factor, the max candidate, and avoid the premature exit of the
    #       process when it is being relaunched
    #[4].-event.- a multiprocessing Event to signal the factor broker that a process in the
    #       middle of being relaunched, is ready for termination
    #[5].-segment.- the candidate space for this process
    #@The following variables should be moved to a configuration file@#
    request_queue=Queue() #Receive requests from network clients
    result_queue=Queue() # Receive results from network clients
    job_queue=Queue() #Send jobs and notifications to network clients
    phase1_time=10 #Time to run to get speed of candidate test in this machine
    max_segments=100 #Maximun number of limits
    max_multiplier=10 #Maximun multiplier for the amount of candidates in a segment
    thres_time_daemon=70 #Time in seconds from which we should start accepting remote clients
    #@The previous variables should be moved to a configuration file@#
    results_dirty=list() #A list of lists with the results of every segment
    num_cpus=multiprocessing.cpu_count() #Number of CPUs in this computer
    while list_of_nums_to_factor:
        num_to_factor=list_of_nums_to_factor.pop(0)
        if arguments.verbose: print "++Factoring: %d" % num_to_factor
        max_candidate=int(math.ceil(math.sqrt(num_to_factor))) #Square root of the number to factor
        top=min(top,max_candidate) #The last possible candidate is the minimum between this two
        # A factoring process is created and run for an specific amount of time to meassure
        # how many factors the program can process in that time.  Based on that data, the
        # segments are created

        # PHASE 1 ######
        factor_eng.append(create_process(num_to_factor,manager,cond,(bottom,top),phase1=True))
        factor_eng[-1][1].start()
        factor_eng[-1][1].join(phase1_time) #Run the process for a specific period of time
        factor_eng[-1][3].acquire() #Lock the updates in the factoring process
        if factor_eng[-1][1].is_alive(): #If factoring is not done
            factor_eng[-1][1].join(0.1) #Just in case it finished between the if and the acquire
            factor_eng[-1][4].clear() #Clear the event in case it was set from the shell
            os.kill(factor_eng[-1][1].pid,signal.SIGUSR1) #Send signal 10 to the process
            factor_eng[-1][4].wait() #Wait for the process to gather and return its data
            factor_eng[-1][1].terminate()
            if factor_eng[-1][2].compnum: #There might be a new composite number to factor here
                num_to_factor=factor_eng[-1][2].compnum
            candidates_processed= (factor_eng[-1][2].last_candidate) - bottom
            if arguments.verbose: print "Candidates processed in phase 1: %d" % candidates_processed
            l_candidate=int(math.ceil(math.sqrt(factor_eng[-1][2].compnum)))
            remaining_candidates=l_candidate - factor_eng[-1][2].last_candidate
            if arguments.verbose: print "Remaining candidates: %d" % remaining_candidates
            groups_of_candidates= remaining_candidates / candidates_processed 
            if groups_of_candidates > max_segments:
                seg_mul_computed=remaining_candidates / float(max_segments*candidates_processed)
                segment_multiplier=min(max_multiplier,seg_mul_computed)
                candidates_per_segment=int(math.ceil(segment_multiplier*candidates_processed))
            else:
                candidates_per_segment=candidates_processed
            if arguments.verbose: print "Candidates per segment:",candidates_per_segment
            if arguments.verbose: print "Last possible candidate:", l_candidate
            segment_low_limit=factor_eng[-1][2].last_candidate
            segment_high_limit=min(segment_low_limit + candidates_per_segment,l_candidate) 
            segments.append((segment_low_limit,segment_high_limit))
            while segment_high_limit < l_candidate:
                segment_low_limit = segment_high_limit + 1
                segment_high_limit=min(segment_low_limit + candidates_per_segment,l_candidate) 
                segments.append((segment_low_limit,segment_high_limit))
        # END OF PHASE 1 ######
        if arguments.verbose: 
            print "Factors found in phase 1: %s" % factor_eng[-1][0]
            print "Number of segments: %d" % len(segments)
        slots=min(num_cpus,len(segments))
        remaining_time = groups_of_candidates * phase1_time * 1.11 / slots if segments else 0
        print "Remaining time %d" % remaining_time
        if remaining_time > thres_time_daemon: 
            if arguments.verbose: print "Daemonize"
            daemon=Process(target=NetCodePrimeF.server_netcode,args=(request_queue,result_queue,job_queue))
            daemon.start()
        else: daemon=None
        running_processes=list()
        cond.acquire()
        while segments or pending_remote_segments: # While segments available
            while slots: # While slots available
                if segments:
                    pick_segment=random.randint(0,len(segments)-1)
                    working_segment=segments.pop(pick_segment)
                else:
                    if arguments.verbose: print "Stealing segment from pending remote client"
                    pick_segment=random.randint(0,len(pending_remote_segments)-1)
                    working_segment=pending_remote_segments.pop(pick_segment)
                factor_eng.append(create_process(num_to_factor,manager,cond,working_segment))
                running_processes.append(factor_eng[-1])
                factor_eng[-1][1].start()
                if arguments.verbose:
                    print "  +Starting process %s in segment %s" % (factor_eng[-1][1].name,factor_eng[-1][5])
                slots -=1
            while not request_queue.empty() and segments: #Serve remote clients requests
                reqres_object=request_queue.get_nowait()
                pick_segment=random.randint(0,len(segments)-1)
                remote_segment=segments.pop(pick_segment)
                # The segments delegated to the remote clients are in the
                # pending_remote_segments list, once the results are returned they must be
                # removed from there.  
                pending_remote_segments.append(remote_segment)
                reqres_object.job_type='RESPONSE'
                reqres_object.num=num_to_factor
                reqres_object.segment=remote_segment
                job_queue.put(reqres_object)
            while not result_queue.empty(): #We got results from the clients
                result_job=result_queue.get_nowait()
                if result_job.is_result() and result_job.results and result_job.segment in pending_remote_segments:
                    if arguments.verbose: print "Job result received in parent: %s " % result_job
                    factor_eng.append([result_job.results])
                    pending_remote_segments.remove(result_job.segment)
                else:
                    print "Some problem with Job result in parent: %s" % result_job
            cond.wait() #Wait for any of the factoring process to finish
            print "Woken up at %.2f" % time.time()
            temp_proc_list=list()
            for proc in running_processes: #Look for the finished process
                proc[1].join(0.08)
                proc[3].acquire()
                if proc[2].end_of_process: #The process has finished factoring
                    print "  -Process %s is finished, with factors %s in segment %s:" % (proc[1].name,proc[0],proc[5])
                    if len(proc[0]) > 1: # There's at least one factor, should be two
                        list_of_nums_to_factor.extend(list(set(proc[0]))) #Add the factor to the list of pending compound numbers
                        for dying_process in running_processes: #Kill all the running processes, even the dead ones
                                                                # Maybe some other process also found some factors,
                                                                # no problem they are kept in factor_eng for later
                                                                # checking 
                            print "killing %s" % dying_process[1].name
                            dying_process[1].terminate()
                            segments=pending_remote_segments=[] #Scratch all the segments
                            bottom=2
                        finish_daemon(daemon)
                        print "Finished"
                        temp_proc_list=[] # Empty the temp list so we end faster
                        break #No more running processes, they are all dead 
                else: #Keep this one
                    temp_proc_list.append(proc)
                    proc[3].release()
            running_processes=temp_proc_list
            slots = min(num_cpus - len(running_processes) , max(len(segments),len(pending_remote_segments)))
        cond.release()
        for last_proc in running_processes:
            last_proc[1].join()
            print "\tProcess is finished:",last_proc[1].name,last_proc[0],last_proc[5]
        #@Signal the daemon to cancel the remote clients@#
    finish_daemon(daemon) #Shutdown the network daemon
    for r in factor_eng: #Collect the factors found in each segment
        results_dirty.append(r[0][:]) #Get the results from every process
    return clean_results(results_dirty,orig_num_to_factor)
    
#Parameters: daemon process reference
#Return value: None
def finish_daemon(daemon):
    '''Connects to the network "twisted" daemon and sends a shutdown request'''
    if daemon and daemon.is_alive():
        print "Closing down daemon..."
        import socket
        s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        s.connect(('localhost',NetCodePrimeF.internal_port))
        s.settimeout(0.5)
        try:
            s.sendall("This is just a test\r\n")
            s.close()
        except socket.timeout:
            print "Socket timeout, just kill the bastard"
            daemon.terminate()
    elif arguments.verbose:
        print "Daemon is not alive, no need to close it"

#Parameters: num_to_factor.- The number to factor
#            manager.- a multiprocessing manager to share variables among processes
#            cond.- multiprocessing condition
#            segment.- the segment limiting the group of candidates to try
#            phase1.- Is this process running in phase1 mode?, default is False
def create_process(num_to_factor,manager,cond,segment,phase1=False):
    '''Creates a process and its accompanying variables'''
    own_results=manager.list() #The list of found factars in this segment, one for every process
    nms=manager.Namespace() #Namespace to create variables across processes, one for every process
    nms.end_of_process=False
    loc=Lock() #A lock to controll access to results (factors found), one for every process
    event=Event() #An event object to set when the process is ready to die, one for every process
    job=Process(target=factorize_with_limits,args=(num_to_factor,own_results,nms,loc,event,cond,segment[0],segment[1],phase1))
    return [own_results,job,nms,loc,event,segment]


#####MAIN#######

#pdb.set_trace()  #Uncomment to debug

if __name__ == '__main__':
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
        if arguments.verbose:
            print "\n+Number to factor=%d" % arguments.num
        t_start=time.time()
        try:
            factors=factor_broker(arguments.num,arguments.firstcandi,arguments.lastcandi)
        except KeyboardInterrupt:
            t_end=time.time()
            print "Time used",round(t_end-t_start,4),"seconds"
            raise
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
            print "Or some factor is not prime"
            exit(-1)
