# Python image to use.
FROM python

# Set the working directory to /app
WORKDIR /app

# Copy the working directory contents into the container at /app
COPY . .

# Install any needed os or python packages specified in Makefile target build
RUN make install

# Run app.py when the container launches
ENTRYPOINT ["python", "app.py"]
