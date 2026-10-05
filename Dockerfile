#Image for the prime factoring server (PrimeFactor.py), based on Red Hat UBI 9 with python 3.12
#The base image already runs as a non root user (UID 1001) inside a python virtual environment
FROM registry.access.redhat.com/ubi9/python-312
LABEL maintainer="Tale Toul <tale.toul@gmail.com>"
ENV AP=/opt/app-root/src/PrimeFactor/
#Twisted is required; gmpy2 is optional (PrimeFactor.py falls back to a pure python primality test)
RUN pip install --no-cache-dir Twisted gmpy2
COPY *.py $AP
WORKDIR $AP
ENTRYPOINT ["./PrimeFactor.py"]
