# syntax=docker/dockerfile:1
#Phrixus.io
FROM python:3

WORKDIR /usr/src/

COPY requirements.txt ./
RUN pip3 install --no-cache-dir -r requirements.txt
COPY . .
RUN printf "deb-src http://http.kali.org/kali kali-rolling main contrib non-free" >> /etc/apt/sources.list
RUN printf "deb http://http.kali.org/kali kali-rolling main contrib non-free" >> /etc/apt/sources.list
#apt-key adv --keyserver keyserver.ubuntu.com --recv-keys ED444FF07D8D0BF6
#RUN apt-key adv --keyserver keyserver.ubuntu.com --recv-keys ED444FF07D8D0BF6
RUN wget "https://http.kali.org/kali/pool/main/k/kali-archive-keyring/kali-archive-keyring_2022.1_all.deb"
RUN dpkg -i kali-archive-keyring_2022.1_all.deb
RUN apt update
RUN apt install nmap -y
#CMD [ "apt-get", "update" ]
#CMD [ "apt-get", "install","nmap","-y" ]


WORKDIR /usr/src/app/back-end/
CMD [ "python3", "web-server.py" ]

EXPOSE 5000
