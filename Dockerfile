FROM ubuntu:latest

RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get -y install \
    apache2 libapache2-mod-wsgi python-pip git vim

# Enable apache mods.
RUN a2enmod wsgi
RUN mkdir -p /log/apache2

# This stopped working
#ENV APACHE_LOG_DIR /logs/apache2
# So APACHE_LOG_DIR is modified now in apache/envvars
ADD apache/envvars /etc/apache2/

ADD apache/000-default.conf /etc/apache2/sites-enabled/000-default.conf
ADD apache/ports.conf /etc/apache2/ports.conf

# Expose apache.
EXPOSE 80

# Copy this repo into place.
ADD ./docs /docs
ADD ./app /web

RUN pip install -r /web/requirements/production.txt
RUN cd /web \
  && NO_CONNECT=1 python manage.py collectstatic --noinput
# confirm settings with apachectl -t -D DUMP_RUN_CFG in the container

CMD ["/usr/sbin/apache2ctl", "-DFOREGROUND"]

