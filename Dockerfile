FROM python:3.11

# Install necessary dependencies for building mysqlclient
# RUN apt-get update && apt-get install -y \
#     pkg-config \
#     libmysqlclient-dev \
#     build-essential \
#     && rm -rf /var/lib/apt/lists/*

# Set the working directory
WORKDIR /BIZCONNECT

# Copy requirements
COPY requirements.txt /BIZCONNECT/

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . /BIZCONNECT/

# Command to run the Django development server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
