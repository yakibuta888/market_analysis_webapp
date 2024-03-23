# syntax=docker/dockerfile:1.4.1
FROM python:3.11-slim

ENV DISPLAY=:1
ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update \
	&& apt-get install -y --no-install-recommends \
	apt-utils \
	gcc \
	build-essential \
	sudo \
	# google-chromeインストール時に必要
	wget \
	unzip \
	gnupg2 \
	# コンテナのGUIをブラウザで表示するためのパッケージ
	tigervnc-standalone-server \
	tigervnc-common \
	tigervnc-tools \
	novnc \
	websockify \
	task-xfce-desktop \
	dbus-x11 \
	x11-utils \
	x11-xserver-utils \
	x11-apps \
	# 日本語環境
	task-japanese \
	locales \
	fonts-takao \
	task-japanese-desktop \
	ibus-kkc \
	# clean up
	&& apt-get autoremove -y \
	&& apt-get clean -y \
	&& rm -rf /var/lib/apt/lists/*

# 日本語設定
RUN sed -i -E 's/# (ja_JP.UTF-8)/\1/' /etc/locale.gen \
	&& locale-gen
ENV LANG ja_JP.UTF-8
ENV LANGUAGE ja_JP:ja
ENV LC_ALL ja_JP.UTF-8

# Google Chrome をインストール
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google-chrome.list \
    && apt-get update \
    && apt-get install -y google-chrome-stable \
    && rm -rf /var/lib/apt/lists/*

ARG WORKDIR
ENV PATH=${WORKDIR}/vendor/bin:$PATH \
	PYTHONPATH=${WORKDIR}/vendor/bin:${WORKDIR} \
	PYTHONUSERBASE=${WORKDIR}/vendor

WORKDIR ${WORKDIR}

# Libraries used only when developing
RUN pip install --upgrade pip;\
	pip install --no-cache-dir \
	autopep8 \
	flake8 \
	pytest

# Create the user
ARG USERNAME
ARG HOMEDIR
ARG USERID
ARG GROUPID
RUN <<-EOF
	echo "Create User = ${USERID}. Group = ${GROUPID}"
	groupadd -g ${GROUPID} ${USERNAME}
	useradd -m -s /bin/bash -d ${HOMEDIR} -k /etc/skel -u ${USERID} -g ${GROUPID} ${USERNAME}
	echo ${USERNAME} ALL=\(root\) NOPASSWD:ALL > /etc/sudoers.d/${USERNAME}
	chmod 0440 /etc/sudoers.d/${USERNAME}
EOF
USER ${USERNAME}
