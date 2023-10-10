# 2021/10/13 by face0u0

FROM python:3.11.6-bullseye

# update apt repository
RUN apt-get update

ENV DEBIAN_FRONTEND=noninteractive
RUN ln -sf /usr/share/zoneinfo/Asia/Tokyo /etc/localtime

WORKDIR /setup 

# https://github.com/analogdevicesinc/libiio/blob/master/README_BUILD.md
RUN \
    apt-get install build-essential -y && \
    apt-get install libxml2-dev bison flex libcdk5-dev cmake git -y && \
    apt-get install libaio-dev libusb-1.0-0-dev -y && \
    apt-get install libserialport-dev libavahi-client-dev -y && \
    apt-get install doxygen graphviz -y && \
    apt-get clean
RUN \
    git clone https://github.com/pcercuei/libini.git && \
    cd libini && \
    mkdir build && \
    cd build && \
    cmake ../ && \
    make && \
    make install
RUN \
    apt-get install python3-setuptools -y && \
    git clone https://github.com/analogdevicesinc/libiio.git -b v0.25 && \
    cd libiio && \
    mkdir build && \
    cd build && \
    cmake ../ -DPYTHON_BINDINGS=ON -DWITH_ZSTD=OFF && \
    make && \
    make install

# install python iio with other library
# https://wiki.analog.com/resources/tools-software/linux-software/pyadi-iio
RUN \
    pip install pylibiio pyadi-iio matplotlib numpy numba scipy wave scikit-commpy && \
    apt-get install python3-tk -y && \
    apt-get clean 

# install some tools
RUN apt-get install gosu cu sudo -y && apt-get clean 

ADD entrypoint.sh /entrypoint.sh
RUN chmod 700 /entrypoint.sh
WORKDIR /app
ENTRYPOINT ["/entrypoint.sh"]
