class NetJob:

    def __init__(self,worker_ID,job_type,num=None,segment=None,results=None):
        self.worker_ID=worker_ID #md5 hash, str type
        self.job_type=job_type #One of: request; response; result
        self.num=num #Number to factor
        self.segment=segment # Segment to look for factors in
        self.results=results # List of factors found 
