FROM fluent/fluentd
USER root
RUN rm /fluentd/etc/fluent.conf
ADD fluent.conf /fluentd/etc/fluent.conf
RUN ["gem", "install", "fluent-plugin-elasticsearch", "--no-document"]
USER fluent