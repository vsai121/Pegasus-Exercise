FROM ubuntu
RUN apt-get update
RUN apt-get install -y python3
RUN apt-get install -y python3-pip
RUN pip3 install -U emojis
ADD ./bin/add_thumbs_up.py /usr/bin/add_thumbs_up.py
RUN chmod +x /usr/bin/add_thumbs_up.py
