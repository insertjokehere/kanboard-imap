FROM python:3.4

RUN cd /tmp && git clone https://github.com/insertjokehere/kanboard-py.git && cd kanboard-py && python ./setup.py install && cd && rm -rf /tmp/kanboard-py

RUN cd /tmp && git clone https://github.com/insertjokehere/kanboard-imap && cd kanboard-imap && python ./setup.py install && cd && rm -rf /tmp/kanboard-imap

CMD kanboard_imap
