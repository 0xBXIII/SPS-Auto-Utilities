FROM python:3.9.6

RUN apt update && apt install -y \
  cron \
  && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt
COPY sps-auto-utilities.py /app/sps-auto-utilities.py
COPY cron-wrapper.sh /app/cron-wrapper.sh
COPY sps-auto-cron /etc/cron.d/sps-auto-cron
RUN crontab /etc/cron.d/sps-auto-cron

CMD ["cron", "-f"]