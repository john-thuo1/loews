# base image
FROM python:3.12.3-slim-bookworm  

ENV PYTHONBUFFERED=1   

WORKDIR /loews   

COPY requirements.txt requirements.txt   

RUN pip3 install --no-cache-dir -r requirements.txt

COPY . .   

EXPOSE 3000

# Copy datasets into the container( only necessary if large files to avoid multiple reruns with every update)
COPY Datasets /loews/Datasets


CMD ["sh", "-c", "python manage.py makemigrations && \
                  python manage.py migrate && \
                  echo \"from django.contrib.auth.models import User; \
                  User.objects.filter(username='$DB_USERNAME').exists() or \
                  User.objects.create_superuser('$DB_USERNAME', '$DB_EMAIL', '$DB_PASSWORD')\" \
                  | python manage.py shell && \
                  python manage.py runserver 0.0.0.0:3000"]