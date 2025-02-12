FROM python:3.11-bullseye

# Install system dependencies for Playwright
RUN apt-get update && apt-get install -y \
    curl \
    gnupg \
    && curl -sL https://deb.nodesource.com/setup_18.x | bash - \
    && apt-get update && apt-get install -y \
    nodejs \
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
    libpango-1.0-0 \
    libcairo2 \
    libgstreamer1.0-0 \
    libgstreamer-plugins-base1.0-0 \
    libxcursor1 \
    libgtk-3-0 \
    # Additional missing dependencies
    libwoff1 \
    flite1-dev \
    libharfbuzz-icu0 \
    libenchant-2-2 \
    libsecret-1-0 \
    libhyphen0 \
    libmanette-0.2-0 \
    libegl1 \
    libgudev-1.0-0 \
    libgles2 \
    x264 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install pip requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install playwright and browser with all dependencies
ENV DEBIAN_FRONTEND=noninteractive
RUN playwright install-deps
RUN playwright install chromium --with-deps

# Copy the rest of the application
COPY . .

# Expose the port the app runs on
ENV PORT=7860
EXPOSE 7860

# Command to run the application
CMD ["python", "app.py"] 