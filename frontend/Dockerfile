# syntax=docker/dockerfile:1.4.1
FROM node:16.20-bullseye

RUN apt-get update \
	&& apt-get install -y --no-install-recommends \
	apt-utils \
	gcc \
	build-essential \
	sudo \
	# clean up
	&& apt-get autoremove -y \
	&& apt-get clean -y \
	&& rm -rf /var/lib/apt/lists/*

ARG WORKDIR
WORKDIR ${WORKDIR}

# Installing packages
COPY package.json .
RUN npm install \
	express@4.18.1 \
	morgan@1.10.0 \
	express-async-errors@3.1.1 \
	mysql2@2.3.3;\
	npm install --save-dev \
	typescript@4.8.3 \
	ts-node@10.9.1 \
	@types/express@4.17.14 \
	nodemon@2.0.20 \
	@types/morgan@1.9.3

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
