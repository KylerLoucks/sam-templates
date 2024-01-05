# Stage 1: Build mdbtools in a Debian-based image
FROM debian:buster as builder

RUN apt-get update && apt-get install -y \
    gcc \
    make \
    autoconf \
    automake \
    libtool \
    bison \
    flex \
    texinfo \
    git \
    autoconf-archive \
    pkg-config \
    gettext \
    gawk

RUN git clone https://github.com/mdbtools/mdbtools.git /mdbtools

WORKDIR /mdbtools
RUN autoreconf -i -f \
    && ./configure \
    && make \
    && make install

# Stage 2: Setup the AWS Lambda image
FROM public.ecr.aws/lambda/python:3.10

# Copy mdbtools binaries from the builder stage
COPY --from=builder /usr/local/bin/ /usr/local/bin/
COPY --from=builder /usr/local/lib/ /usr/local/lib/

# Set LD_LIBRARY_PATH to include /usr/local/lib
ENV LD_LIBRARY_PATH=/usr/local/lib:$LD_LIBRARY_PATH

# Copy the Python function code
COPY requirements.txt ${LAMBDA_TASK_ROOT}

RUN pip install -r requirements.txt

COPY app.py ${LAMBDA_TASK_ROOT}


# Command can be overwritten by providing a different command in the template directly.
CMD [ "app.handler" ]