FROM python:3.10-slim

WORKDIR /app
COPY . .
COPY docker-entrypoint.sh /usr/local/bin/
RUN chmod +x /usr/local/bin/docker-entrypoint.sh

RUN pip install --no-cache-dir -r requirements.txt
ENV FLASK_ENV production
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:8000", "app:app", "--access-logfile", "-"]
ENTRYPOINT ["/usr/local/bin/docker-entrypoint.sh"]