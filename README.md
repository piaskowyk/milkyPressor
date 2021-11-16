windows WSL, ubuntu

sudo apt-get install git build-essential cmake libmbedtls-dev zlib1g-dev

git clone https://github.com/AVSystem/Anjay.git \
    && cd Anjay \
    && git submodule update --init \
    && cmake . \
    && make -j \
    && ./output/bin/demo --endpoint-name $(hostname) --server-uri coap://try-anjay.avsystem.com:5683


git clone https://github.com/AVSystem/Anjay.git
cd Anjay
git submodule update --init
cmake . && make && sudo make install

https://github.com/eclipse/leshan#test-server-sandbox
java -jar ./leshan-server-demo.jar

https://github.com/darkopetrovic/lwm2m-web-server
https://github.com/lwmqn/shepherd