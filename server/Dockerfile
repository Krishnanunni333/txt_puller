FROM python:3.10
RUN apt-get update
WORKDIR /txt_puller
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY . .
RUN mkdir alltxtfiles
RUN mkdir filemetadata
ENTRYPOINT [ "python" ]
CMD ["app.py" ]
EXPOSE 5000