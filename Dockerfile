FROM python:3.11

# Copy the requirements.txt file into the container
COPY requirements.txt .

# Install the Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the marimo notebook
COPY science.py science.py

# Run the marimo notebook
ENTRYPOINT ["marimo", "run", "--host", "0.0.0.0", "--port", "80", "--headless"]
