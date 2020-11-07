FROM python:3.8.6-slim-buster

EXPOSE 5000

WORKDIR /home/blog

COPY . /home/blog

RUN pip install -r requirements.txt
RUN pip install gunicorn

ENV IMAGE_UPLOADS=/img

VOLUME [ "/img" ]

RUN flask db upgrade
CMD [ "gunicorn", "--bind", "0.0.0.0:5000", "bloggy:app" ]