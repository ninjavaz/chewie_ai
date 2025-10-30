FROM python:3.11-slim

WORKDIR /app

# Install system dependencies including Playwright dependencies
RUN apt-get update && apt-get install -y \
    gcc g++ postgresql-client curl \
    libnss3 libnspr4 libatk1.0-0 libatk-bridge2.0-0 \
    libcups2 libdrm2 libdbus-1-3 libxkbcommon0 \
    libxcomposite1 libxdamage1 libxfixes3 libxrandr2 \
    libgbm1 libpango-1.0-0 libcairo2 libasound2 \
    libatspi2.0-0 libxshmfence1 fonts-liberation \
    fonts-noto-color-emoji \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install Playwright browsers (deps already installed above)
RUN playwright install chromium

COPY . .

# Make entrypoint script executable
RUN chmod +x /app/scripts/entrypoint.sh

RUN useradd -m -u 1000 chewie && chown -R chewie:chewie /app
USER chewie

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

ENTRYPOINT ["/app/scripts/entrypoint.sh"]