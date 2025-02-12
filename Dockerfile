FROM python:3.11-slim

# Install system dependencies for Playwright
RUN apt-get update && apt-get install -y \
    libnss3 \
    libnspr4 \
    libatk1.0-0 \
    libatk-bridge2.0-0 \
    libcups2 \
    libdrm2 \
    libxkbcommon0 \
    libxcomposite1 \
    libxdamage1 \
    libxfixes3 \
    libxrandr2 \
    libgbm1 \
    libasound2 \
    libx11-6 \
    libxcb1 \
    libxext6 \
    libxcomposite1 \
    libxcursor1 \
    libxdamage1 \
    libxfixes3 \
    libxi6 \
    libxrandr2 \
    libxrender1 \
    libxss1 \
    libxtst6 \
    fonts-liberation \
    # Adding missing GTK and related libraries
    libgtk-3-0 \
    libgdk-pixbuf-2.0-0 \
    libpangocairo-1.0-0 \
    libcairo-gobject2 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install pip requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install playwright and browser
RUN pip install playwright && playwright install chromium --with-deps

# Copy the rest of the application
COPY . .

# Expose the port the app runs on
ENV PORT=7860
EXPOSE 7860

# Command to run the application
CMD ["python", "app.py"] 