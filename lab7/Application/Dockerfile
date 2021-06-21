FROM python

ADD ./requirements.txt /Application/requirements.txt

RUN pip install -r ./Application/requirements.txt

# RUN wget https://github.com/prometheus/node_exporter/releases/download/v1.1.2/node_exporter-1.1.2.darwin-amd64.tar.gz \
# && tar xvfz node_exporter-*.*-amd64.tar.gz \
# && cd node_exporter-1.1.2.darwin-amd64

EXPOSE 5000
# EXPOSE 9100

ADD ./ /Application

ENTRYPOINT [ "python", "Application/app.py"]
