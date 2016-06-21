class NetJob:


    #Parameters: worker_ID.- MD5 hash identifing the object
    #            job_type.- one of 'REQUEST' 'RESPONSE' 'RESULT'
    #            num.- number to factor
    #            segment.- Segment to look for factors in
    #            results.- List of factors found
    def __init__(self,worker_ID,job_type,num=None,segment=None,results=None):
        self.worker_ID=worker_ID #md5 hash, string type
        self.job_type=job_type 
        self.num=num 
        self.segment=segment 
        self.results=results 
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
        my_representation="Worker_ID: %s Job_type: %s Num: %d Segment: %s Results: %s" % (self.worker_ID,self.job_type,self.num, self.segment, self.results)
        return my_representation

    def add_results(self,found_results):
        if self.is_response():
            self.results=found_results
            self.job_type=self.job_type_dict['result']
        else:
            raise Exception("Cannot add results to non response NetJob")
