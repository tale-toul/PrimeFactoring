class NetJob:

    job_type_dict={'request': 'REQUEST',
            'response': 'RESPONSE',
            'result': 'RESULT'}

    #Parameters: worker_ID.- MD5 hash identifing the object
    #            job_type.- one of 'REQUEST' 'RESPONSE' 'RESULT'
    #            num.- number to factor
    #            segment.- Segment to look for factors in
    #            results.- List of factors found
    def __init__(self,worker_ID,job_type,num=None,segment=None,results=None):
        self.worker_ID=worker_ID #md5 hash, str type
        self.job_type=job_type 
        self.num=num 
        self.segment=segment 
        self.results=results 

    
    def is_request(self):
        '''Is this object a request?'''
        return self.job_type == job_type_dict['request'] 

    def is_response(self):
        '''Is this object a response?'''
        return  self.job_type == job_type_dict['response'] 

    def is_result(self):
        '''Is this object a result?'''
        return self.job_type == job_type_dict['result'] 
