# Get base image.
FROM python:3.9-slim-buster

ENV PYTHONUNBUFFERED 1
ENV TZ=Asia/Bangkok

RUN apt-get update && apt-get install -y build-essential \
      gcc \
      netcat-openbsd libc6-dev \
      libpq-dev  \
      musl-dev \
      python3-psycopg2 && \
    rm -rf /var/cache/apt/* /var/lib/apt/lists/* && \
    # timezone
    ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && \
    echo $TZ > /etc/timezone

# install dependencies
COPY . /build
WORKDIR /build
RUN pip install install -r dependencies/requirements-dev.txt

EXPOSE 8000

# # Start the service
CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]