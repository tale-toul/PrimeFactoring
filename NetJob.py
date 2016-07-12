import md5
import datetime

class NetJob:


    #Parameters: worker_ID.- MD5 hash identifying the client this worker belongs to
    #            job_type.- one of 'REQUEST' 'RESPONSE' 'RESULT'
    #            num.- number to factor
    #            segment.- Segment to look for factors in
    #            results.- List of factors found
    #            job_ID.- MD5 hash identifying this object
    def __init__(self,worker_ID,job_type,num=1,segment=(),results=[]):
        self.worker_ID=worker_ID #md5 hash, string type
        self.job_type=job_type 
        self.num=num 
        self.segment=segment 
        self.results=results 
        self.job_ID=md5.new(str(self.worker_ID) + str(datetime.datetime.now())).hexdigest()
        self.job_type_dict={'request': 'REQUEST',
                            'response': 'RESPONSE',
                            'result': 'RESULT',
                            'ack': 'ACK'}
    
    def is_request(self):
        '''Is this object a request?'''
        return self.job_type == self.job_type_dict['request'] 

    def is_response(self):
        '''Is this object a response?'''
        return  self.job_type == self.job_type_dict['response'] 

    def is_result(self):
        '''Is this object a result?'''
        return self.job_type == self.job_type_dict['result'] 

    def is_ack(self):
        '''Is this object an ACK'''
        return self.job_type == self.job_type_dict['ack']

    def __repr__(self):
        my_representation="Worker_ID:%s Job_type:%s Num:%d Segment:%s Results:%s Job_ID:%s" % (self.worker_ID[:7],self.job_type,self.num, self.segment, self.results, self.job_ID[:7])
        return my_representation

    def add_results(self,found_results):
        if self.is_response():
            self.results=found_results
            self.job_type=self.job_type_dict['result']
        else:
            raise Exception("Cannot add results to non response NetJob")
