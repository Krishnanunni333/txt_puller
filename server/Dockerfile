FROM python:3.10
RUN apt-get update
RUN apt-get install -y git
RUN git clone https://github.com/Krishnanunni333/txt_puller.git
WORKDIR /root/txt_puller
RUN pip install -r requirements.txt
ENTRYPOINT [ "python" ]
CMD ["./server/app.py" ]