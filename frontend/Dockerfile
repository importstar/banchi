FROM debian:sid
# RUN echo 'deb http://mirrors.psu.ac.th/debian/ sid main contrib non-free' > /etc/apt/sources.list
RUN echo 'deb http://mirror.kku.ac.th/debian/ sid main contrib non-free non-free-firmware' > /etc/apt/sources.list
RUN apt update && apt upgrade -y
RUN apt install -y python3 python3-dev python3-pip python3-venv npm git locales
# RUN sed -i '/th_TH.UTF-8/s/^# //g' /etc/locale.gen && locale-gen
# ENV LANG th_TH.UTF-8 
# ENV LANGUAGE th_TH:en 
# ENV LC_ALL th_TH.UTF-8


RUN python3 -m venv /venv
ENV PYTHON=/venv/bin/python3

RUN $PYTHON -m pip install poetry gunicorn


WORKDIR /app/clients/banchi-client
ADD clients/banchi-client /app/clients/banchi-client
RUN $PYTHON -m poetry config virtualenvs.create false && $PYTHON -m poetry install --no-interaction --only main

WORKDIR /app
COPY frontend/banchi/cmd /app/banchi/cmd
COPY frontend/poetry.lock frontend/pyproject.toml frontend/README.md /app/
RUN $PYTHON -m poetry config virtualenvs.create false && $PYTHON -m poetry install --no-interaction --only main

COPY frontend/banchi/web/static/package.json frontend/banchi/web/static/package-lock.json banchi/web/static/
RUN npm install --prefix banchi/web/static

COPY frontend /app



# RUN ln -s $(command -v python3) /usr/bin/python
# RUN pip3 install poetry
# RUN poetry config virtualenvs.create false && poetry install --no-interaction

# For brython
# RUN cd /app/banchi/web/static/brython; \
#     for i in $(ls -d */); \
#     do \
#     cd $i; \
#     python3 -m brython --make_package ${i%%/}; \
#     mv *.brython.js ..; \
#     cd ..; \
#     done
