FROM debian:sid
RUN echo 'deb http://mirrors.psu.ac.th/debian/ sid main contrib non-free' > /etc/apt/sources.list
# RUN echo 'deb http://mirror.kku.ac.th/debian/ sid main contrib non-free' >> /etc/apt/sources.list

RUN apt update --fix-missing && apt dist-upgrade -y
RUN apt install -y python3 python3-dev python3-pip python3-venv build-essential locales npm

RUN sed -i '/th_TH.UTF-8/s/^# //g' /etc/locale.gen && locale-gen
ENV LANG th_TH.UTF-8
ENV LANGUAGE th_TH:en
# ENV LC_ALL th_TH.UTF-8

RUN python3 -m venv /venv
ENV PYTHON=/venv/bin/python3
RUN $PYTHON -m pip install wheel poetry gunicorn

WORKDIR /app/clients/banchi-client
ADD clients/banchi-client /app/clients/banchi-client

RUN . /venv/bin/activate \
	&& poetry config virtualenvs.create false \
	&& poetry install --no-interaction --only main



WORKDIR /app
COPY banchi/cmd /app/banchi/cmd
COPY poetry.lock pyproject.toml /app/
RUN . /venv/bin/activate \
	&& poetry install --no-interaction --only main

COPY banchi/web/static/package.json banchi/web/static/package-lock.json banchi/web/static/
RUN npm install --prefix banchi/web/static



COPY . /app

# EXPOSE 9000
# ENTRYPOINT [ "/venv/bin/gunicorn",  "-w", "5", "--threads", "5", "--bind", "0.0.0.0:9000", "--worker-class", "uvicorn.workers.UvicornWorker", "--timeout", "600", "--keep-alive", "10", "banchiapi.main:get_application"]
