FROM python

ADD ./requirements.txt /Application/requirements.txt

WORKDIR /Application

RUN pip install -r requirements.txt

EXPOSE 5000

ADD ./ /Application

ENTRYPOINT [ "python"]

CMD [ "app.py" ]
