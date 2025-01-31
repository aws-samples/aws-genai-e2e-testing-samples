#  Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
#  SPDX-License-Identifier: MIT-0
# 
#  Permission is hereby granted, free of charge, to any person obtaining a copy of this
#  software and associated documentation files (the "Software"), to deal in the Software
#  without restriction, including without limitation the rights to use, copy, modify,
#  merge, publish, distribute, sublicense, and/or sell copies of the Software, and to
#  permit persons to whom the Software is furnished to do so.
# 
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED,
#  INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A
#  PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
#  HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
#  OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
#  SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

FROM docker.io/ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive
ENV DEBIAN_PRIORITY=high
ENV ENVIRONMENT=container
ARG geckodriver_ver=0.35.0

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apt-get update && \
    apt-get -y upgrade && \
    apt-get -y dist-upgrade && \
    apt-get -y install \
    gosu \
    # UI Requirements
    xvfb \
    xterm \
    xdotool \
    scrot \
    imagemagick \
    mutter \
    x11vnc \
    # Python/pyenv reqs
    build-essential \
    libssl-dev  \
    zlib1g-dev \
    libbz2-dev \
    libreadline-dev \
    libsqlite3-dev \
    curl \
    git \
    libncursesw5-dev \
    xz-utils \
    tk-dev \
    libxml2-dev \
    libxmlsec1-dev \
    libffi-dev \
    liblzma-dev \
    # Network tools
    net-tools \
    netcat \
    # PPA req
    software-properties-common && \
    # Userland apps
    add-apt-repository ppa:mozillateam/ppa && \
    apt-get install -y --no-install-recommends \
    libreoffice \
    firefox-esr \
    x11-apps \
    xpdf \
    gedit \
    xpaint \
    tint2 \
    poppler-utils \
    galculator \
    pcmanfm \
    unzip && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Download and install geckodriver
RUN apt-get update \
    && apt-get upgrade -y \
    && apt-get install -y && curl -fL -o /tmp/geckodriver.tar.gz \
            https://github.com/mozilla/geckodriver/releases/download/v${geckodriver_ver}/geckodriver-v${geckodriver_ver}-linux64.tar.gz \
    && tar -xzf /tmp/geckodriver.tar.gz -C /tmp/ \
    && chmod +x /tmp/geckodriver \
    && mv /tmp/geckodriver /usr/bin/

# setup user
ENV USERNAME=computeruse
ENV HOME=/home/$USERNAME
RUN useradd -m -s /bin/bash -d $HOME $USERNAME

USER computeruse
WORKDIR $HOME

# setup python
RUN git clone https://github.com/pyenv/pyenv.git ~/.pyenv && \
    cd ~/.pyenv && src/configure && make -C src && cd .. && \
    echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.bashrc && \
    echo 'command -v pyenv >/dev/null || export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bashrc && \
    echo 'eval "$(pyenv init -)"' >> ~/.bashrc
ENV PYENV_ROOT="$HOME/.pyenv"
ENV PATH="$PYENV_ROOT/bin:$PATH"
ENV PYENV_VERSION_MAJOR=3
ENV PYENV_VERSION_MINOR=11
ENV PYENV_VERSION_PATCH=6
ENV PYENV_VERSION=$PYENV_VERSION_MAJOR.$PYENV_VERSION_MINOR.$PYENV_VERSION_PATCH
RUN eval "$(pyenv init -)" && \
    pyenv install $PYENV_VERSION && \
    pyenv global $PYENV_VERSION && \
    pyenv rehash

ENV PATH="$HOME/.pyenv/shims:$HOME/.pyenv/bin:/usr/bin/geckodriver:/usr/bin/firefox-esr:$PATH"

RUN python -m pip install --upgrade pip==23.3 setuptools>=65.0.0 wheel==0.40.0 && \
    python -m pip config set global.disable-pip-version-check true

# only reinstall if requirements.txt changes
COPY --chown=$USERNAME:$USERNAME backend/requirements.txt $HOME/computer_use_poc/requirements.txt
RUN python -m pip install --no-cache-dir -r $HOME/computer_use_poc/requirements.txt

# setup env & app
COPY --chown=$USERNAME:$USERNAME backend/ $HOME/computer_use_poc/
RUN chmod +x $HOME/computer_use_poc/entrypoint.sh

# Remove unnecessary files within the app directory
RUN find $HOME/computer_use_poc -type d -name "__pycache__" -exec rm -rf {} +

USER ${USERNAME}
COPY --chown=$USERNAME:$USERNAME frontend/tests/e2e.yml $HOME/computer_use_poc/tests/e2e.yml

ARG DISPLAY_NUM=1
ARG HEIGHT=768
ARG WIDTH=1024
ARG PROMPT_MODE=file
ARG APP_BASE_URL=http://192.168.178.43:3000
ARG FIREFOX_BINARY_PATH=/usr/bin/firefox-esr
ENV DISPLAY_NUM=$DISPLAY_NUM
ENV HEIGHT=$HEIGHT
ENV WIDTH=$WIDTH
ENV PROMPT_MODE=$PROMPT_MODE
ENV APP_BASE_URL=$APP_BASE_URL
ENV FIREFOX_BINARY_PATH=$FIREFOX_BINARY_PATH

# start the app
WORKDIR $HOME/computer_use_poc

CMD ["/home/computeruse/computer_use_poc/entrypoint.sh"]
