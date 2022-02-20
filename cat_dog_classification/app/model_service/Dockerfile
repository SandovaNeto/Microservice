FROM tensorflow/serving:2.4.1

ENV MODEL_NAME="CAT-DOG"
ENV MODEL_BASE_PATH="/models"

COPY ./prev_trained_models/ /models

EXPOSE 8500
EXPOSE 8501

RUN echo "net.ipv6.conf.all.disable_ipv6=1" | tee -a /etc/sysctl.conf
RUN echo "net.ipv6.conf.default.disable_ipv6=1" | tee -a /etc/sysctl.conf
RUN echo "net.ipv6.conf.lo.disable_ipv6=1" | tee -a /etc/sysctl.conf
RUN echo "net.ipv4.ip_forward=1" | tee -a /etc/sysctl.conf