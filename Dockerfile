FROM conda/miniconda3:latest

ARG gc_key_path="/root/gc-key.json"

# install system-level dependencies, as in: https://github.com/crosbymichael/build-essential-docker
RUN apt update && apt install -y --no-install-recommends \
    make \
    automake \
    gcc \
    build-essential \
    g++ \
    cpp \
    libc6-dev \
    man-db \
    autoconf \
    pkg-config \
    git

# set up Google Cloud credentials
COPY dev/*.json /root/
ENV GOOGLE_APPLICATION_CREDENTIALS=$gc_key_path

# copy utils and install library and install them with all dependencies
COPY requirements.txt /requirements.txt
COPY spacy_pl_utils /spacy_pl_utils
COPY spacy_install /spacy_install
COPY Makefile /Makefile
RUN make install-dependencies
RUN rm -rf /requirements.txt /spacy_pl_utils /spacy_install /Makefile

# running the commands will be set up in docker-compose for clarity with regard to volume locations
CMD echo "Run via docker-compose"
