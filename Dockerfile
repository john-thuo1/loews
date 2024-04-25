# Using Python 3.12 as the base image
FROM python:3.12   

# Set an environment variable to enable unbuffered Python output logging
ENV PYTHONBUFFERED=1   

# Set the working directory inside the container to /loews
WORKDIR /loews   

# Copy the requirements.txt file from the host to the container
COPY requirements.txt requirements.txt   

# Installing Python dependencies specified in requirements.txt
RUN pip3 install -r requirements.txt   

# Copy all files and directories from the host directory(.) to the container's working directory(.)
COPY . .   

# Copy datasets into the container( only necessary if large files to avoid multiple reruns with every update)
COPY Datasets /loews/Datasets

# Run migrations
RUN python manage.py makemigrations
RUN python manage.py migrate

# Create superuser
RUN echo "from django.contrib.auth.models import User; User.objects.create_superuser('admin', 'admin@example.com', 'adhominem1234')" | python manage.py shell

# Command to run the Django development server when the container starts
CMD ["python", "manage.py", "runserver", "0.0.0.0:3000"]
