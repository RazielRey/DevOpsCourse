FROM python:3.9-slim

# Install Chrome dependencies and ChromeDriver
RUN apt-get update && apt-get install -y \
    chromium \
    chromium-driver \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy all test files
COPY . .

# Install dependencies
RUN pip install -r requirements.txt

# Run tests
CMD ["python", "run_tests.py"]