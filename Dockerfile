FROM python:3.11

# Copy the requirements.txt file into the container
COPY requirements.txt .

# Install the Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of application code into the container
COPY . .

# Run the marimo notebook
ENTRYPOINT ["marimo", "run", "science.py", "--host", "0.0.0.0", "--port", "80", "--headless"]
