FROM python:alpine
# instalare modul kafka-python
RUN pip install kafka-python
WORKDIR /bidder
ADD Bidder.py $WORKDIR
CMD ["python", "Bidder.py"]