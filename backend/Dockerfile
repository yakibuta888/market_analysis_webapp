# syntax=docker/dockerfile:1.4.1
FROM python:3.11-slim as builder

ARG WORKDIR
WORKDIR ${WORKDIR}

COPY requirements.txt .
RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt --target=${WORKDIR}/vendor

COPY . .

FROM python:3.11-slim as production

# 必要なパッケージとChromeのインストール
RUN apt-get update && apt-get install -y --no-install-recommends \
	wget \
	gnupg2 \
	&& wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - \
	&& echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google.list \
	&& apt-get update \
	&& apt-get install -y google-chrome-stable \
	&& apt-get autoremove -y \
	&& apt-get clean \
	&& rm -rf /var/lib/apt/lists/*

ARG WORKDIR
ENV PATH=${WORKDIR}/vendor/bin:$PATH \
	PYTHONPATH=${WORKDIR}/vendor:${WORKDIR} \
	PYTHONUSERBASE=${WORKDIR}/vendor
WORKDIR ${WORKDIR}

# Create the user
ARG USERNAME
ARG HOMEDIR
ARG USERID
ARG GROUPID
RUN <<-EOF
	echo "Create User = ${USERID}. Group = ${GROUPID}"
	groupadd -g ${GROUPID} ${USERNAME}
	useradd -m -s /bin/bash -d ${HOMEDIR} -u ${USERID} -g ${GROUPID} ${USERNAME}
	mkdir -p /etc/sudoers.d/
	echo ${USERNAME} ALL=\(root\) NOPASSWD:ALL > /etc/sudoers.d/${USERNAME}
	chmod 0440 /etc/sudoers.d/${USERNAME}
EOF
USER ${USERNAME}

# ビルドステージからコピーした依存関係とアプリケーションのソースコードをコピー
COPY --from=builder ${WORKDIR} ${WORKDIR}

# 環境変数の設定
# Pythonがpycファイルとdiscへの書き込みを行わないようにする
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# アプリケーションの起動コマンド
CMD ["gunicorn", "-k", "uvicorn.workers.UvicornWorker", "src.main:app", "--bind", "0.0.0.0:8000", "--workers", "4"]
