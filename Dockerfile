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

RUN python manage.py makemigrations
RUN python manage.py migrate

RUN echo "from django.contrib.auth.models import User; \
          User.objects.filter(username='admin').exists() or \
          User.objects.create_superuser('admin', 'admin@example.com', 'avatar1234!')" \
          | python manage.py shell

CMD ["python", "manage.py", "runserver", "0.0.0.0:3000"]
