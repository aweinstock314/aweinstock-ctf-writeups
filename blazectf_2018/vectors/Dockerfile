FROM ubuntu:trusty
RUN sudo apt-get update
RUN sudo apt-get install -y socat

RUN adduser vectors
COPY prod/* /tmp/vectors/
WORKDIR /tmp/vectors

EXPOSE 1337
USER vectors
CMD socat TCP-LISTEN:1337,reuseaddr,fork EXEC:"./vectors"
