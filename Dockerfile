FROM mcr.microsoft.com/playwright/python:v1.41.0-jammy

WORKDIR /app

# Install pip requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Expose the port the app runs on
ENV PORT=7860
EXPOSE 7860

# Command to run the application
CMD ["python", "app.py"] 