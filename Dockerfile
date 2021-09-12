# syntax=docker/dockerfile:1

FROM python:3.8

RUN mkdir /rl_ltl_pac
WORKDIR rl_ltl_pac


RUN  apt-get update \
  && apt-get install -y wget unzip gnupg2 build-essential openjdk-11-jdk \
  && rm -rf /var/lib/apt/lists/*

RUN wget http://www.lrde.epita.fr/dload/spot/spot-2.9.6.tar.gz; \
	tar -xvzf spot-2.9.6.tar.gz; \
	cd spot-2.9.6; \
	./configure; \
	make -j 8; \
	make install; \
	cd ..

RUN wget https://owl.model.in.tum.de/files/owl-20.06.00.zip -O owl-20.06.zip
RUN unzip owl-20.06.zip

COPY mungojerrie mungojerrie
RUN apt-get update; apt-get upgrade; apt-get install -y flex bison
RUN apt-get install -y libboost-all-dev
RUN cd mungojerrie; \
	mkdir build; cd build; \
	../configure --with-spot=/usr/local --with-owl=/rl_ltl_pac/owl-20.06/ --prefix=/usr/local --enable-silent-rules  --enable-shared --enable-openmp; \
	make -j 8 

RUN pip install matplotlib numpy scipy \
		tqdm num2tex graphviz jupyterlab
RUN pip install ipywidgets

COPY rl_ltl_pac.ipynb rl_ltl_pac.ipynb

COPY models models

CMD jupyter notebook rl_ltl_pac.ipynb --ip 0.0.0.0 --port 8081 --no-browser --allow-root
