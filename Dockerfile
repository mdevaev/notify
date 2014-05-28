# Base GNS image

FROM yandex/ubuntu-pypy3:latest
MAINTAINER Devaev Maxim <mdevaev@gmail.com>

# XXX: OSError: Cannot load library
# /opt/pypy3/lib_pypy/_tkinter/__pycache__/_cffi__gd85ebb05xcf53ad51.pypy-23.so:
# libtcl8.5.so.0: cannot open shared object file: No such file or directory
RUN apt-get -y update \
	&& DEBIAN_FRONTEND=noninteractive apt-get install \
		tk \
		libtclcl1 \
		-y --force-yes \
	&& apt-get -y clean

RUN easy_install -H *.python.org git+git://github.com/signalfuse/maestro-ng

ADD . /root/gns
RUN easy_install -H *.python.org /root/gns
RUN cp -r /root/gns/etc/gns-maestro.d /root/gns.d
RUN rm -rf /root/gns

CMD trap exit TERM; gns $GNS_MODULE -c ${GNS_CONFIG:-/root/gns.d/gns.yaml} & wait
