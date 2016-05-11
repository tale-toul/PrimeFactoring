#!/usr/bin/env python
# Tests for multiprocessing Condition

import multiprocessing
import time, random

def condition_func(cond):
    nap=random.randint(1,4)
    print "Sleep time in process",multiprocessing.current_process().name,":",nap
    time.sleep(nap)
    cond.acquire()
    print '\t %s %f' % (str(cond) , time.time())
    time.sleep(2.5)
    print '\tchild is notifying at %f' % time.time()
    cond.notify_all()
    cond.release()
    print '\t %s %f' % (str(cond) , time.time())

def test_condition():
    loc=multiprocessing.Lock()
    cond = multiprocessing.Condition(loc)
    p = multiprocessing.Process(target=condition_func, args=(cond,))
    q = multiprocessing.Process(target=condition_func, args=(cond,))
    cond.acquire()
    print cond
    p.start()
    q.start()
    print 'main is waiting, and releases the lock'
    cond.wait()
    print 'main has woken up, reacquires the lock'
    print cond
    print 'does  some important tasks...'
    time.sleep(4)
    print 'tasks are finished'
    cond.release()
    print cond
    #cond.release()
    p.join()
    q.join()
    #print cond
    print "The End"

if __name__ == '__main__':
    print "Starting"
    test_condition()
