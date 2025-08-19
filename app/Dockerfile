FROM python
WORKDIR /src
COPY . .
EXPOSE 4000
RUN pip install flask
RUN pip install mysql-connector-python==8.4.0
CMD python server.py
