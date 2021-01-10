FROM python:3.8

RUN cat /etc/issue

RUN pip3 install --upgrade pip

COPY ./requirements.txt ./backend/requirements.txt

# install requirements
RUN pip3 install -r ./backend/requirements.txt

RUN rm -r /root/.cache

# copy files and start
COPY . /backend

WORKDIR /backend

CMD ['bash']