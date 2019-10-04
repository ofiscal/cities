FROM debian:latest

ENV LANG=C.UTF-8 LC_ALL=C.UTF-8
ENV PATH /opt/conda/bin:$PATH

RUN echo "2019 09 30"           && \
  apt update --fix-missing   -y && \
  apt upgrade                -y

RUN apt install streamripper -y

RUN PATH=/root/.local/bin:$PATH
EXPOSE 8888
CMD ["/bin/bash"]
