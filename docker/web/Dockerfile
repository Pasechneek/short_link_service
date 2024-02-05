FROM python:3
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN mkdir -p /web
WORKDIR /web

COPY . /web

RUN ["chmod", "+x", "start.sh"]
RUN pip install -r /web/requirements.txt
# --no-cache-dir
CMD ["/web/start.sh"]