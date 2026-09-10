# Imagem única do laboratório. Pequena de propósito: a VM do Cloud Shell é
# efêmera e recicla o cache de imagens — imagem grande = aula perdida no pull.
FROM alpine:3.20

RUN apk add --no-cache \
      iproute2 \
      iputils \
      tcpdump \
      curl \
      busybox-extras \
      openssl \
      netcat-openbsd \
 && mkdir -p /srv /lab \
 && ln -sf /usr/bin/busybox-extras /usr/local/bin/httpd \
 && httpd --help 2>&1 | grep -qi 'usage: httpd'

CMD ["sleep", "infinity"]
