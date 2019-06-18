FROM python:2.7.16

WORKDIR /app

COPY . /app

USER root

RUN chmod 755 /app

RUN pip install --trusted-host pypi.python.org -r requirements.txt

EXPOSE 8888

CMD jupyter notebook --no-browser --ip=0.0.0.0 --allow-root --NotebookApp.token=''

