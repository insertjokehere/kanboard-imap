FROM python:3.4

RUN pip install -U setuptools pip

RUN cd /tmp && git clone https://github.com/insertjokehere/kanboard-py.git && cd kanboard-py && python ./setup.py install && cd && rm -rf /tmp/kanboard-py

RUN cd /tmp && git clone https://github.com/insertjokehere/kanboard-imap && cd kanboard-imap && python ./setup.py install && cd && rm -rf /tmp/kanboard-imap

RUN mkdir /home/kanboard-imap && groupadd -r swuser -g 433 && \
useradd -u 431 -r -g swuser -d /home/kanboard-imap -s /sbin/nologin -c "Docker image user" swuser && \
chown -R swuser:swuser /home/kanboard-imap

ENV REQUESTS_CA_BUNDLE=/etc/ssl/certs/ca-certificates.crt

USER swuser

WORKDIR /home/kanboard-imap

CMD kanboard_imap
