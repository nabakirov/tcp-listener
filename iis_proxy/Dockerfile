FROM ubuntu:latest
# apt-get and system utilities
RUN apt-get update && apt-get install -y \
    curl apt-utils apt-transport-https debconf-utils gcc build-essential g++-5 \
    && rm -rf /var/lib/apt/lists/*

# python libraries
RUN apt-get update && apt-get install -y \
    python3-pip python3-dev python3-setuptools tzdata \
    --no-install-recommends \
    && rm -rf /var/lib/apt/lists/*

# install necessary locales
RUN apt-get update && apt-get install -y locales \
    && echo "en_US.UTF-8 UTF-8" > /etc/locale.gen \
    && locale-gen
RUN pip3 install --upgrade pip
RUN ln -fs /usr/share/zoneinfo/Asia/Bishkek /etc/localtime && dpkg-reconfigure -f noninteractive tzdata

COPY . /opt/iis_proxy/
WORKDIR /opt/iis_proxy/

# fetch app specific deps
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt

# expose port
EXPOSE 4442

# start app
CMD [ "/usr/bin/python3", "./proxyMiddleWare.py", "configs.py" ]
