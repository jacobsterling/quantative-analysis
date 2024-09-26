# Use Python 3.11 as the base image
FROM python:3.11-slim-bullseye

# Set the working directory in the container
WORKDIR /freqtrade

# Install system dependencies
RUN apt-get update && \
    apt-get install -y curl build-essential libssl-dev libffi-dev libatlas-base-dev libopenjp2-7 libtiff5 git && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Install TA-Lib
RUN curl -L http://prdownloads.sourceforge.net/ta-lib/ta-lib-0.4.0-src.tar.gz | tar xvz && \
    cd ta-lib && \
    ./configure --prefix=/usr && \
    make && \
    make install && \
    cd .. && \
    rm -rf ta-lib

# Clone Freqtrade repository
RUN git clone https://github.com/freqtrade/freqtrade.git /tmp/freqtrade && \
    cp -r /tmp/freqtrade/* /freqtrade/ && \
    rm -rf /tmp/freqtrade

# Copy requirements.txt and install Python dependencies
COPY requirements.txt /freqtrade/
RUN pip install --no-cache-dir numpy cython
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir python-dotenv

# Install Freqtrade
RUN pip install -e .

# Copy the configuration module and main.py
COPY configuration /freqtrade/configuration
COPY main.py /freqtrade/main.py
COPY constants.py /freqtrade/constants.py

# Create a non-root user
RUN useradd -m freqtrader
RUN chown -R freqtrader:freqtrader /freqtrade

# Copy and make the startup script executable
COPY start.sh /freqtrade/start.sh
RUN chmod +x /freqtrade/start.sh

# Switch to non-root user
USER freqtrader

# Expose port 8080 for the Freqtrade API
EXPOSE 8080

# Default command (can be overridden by docker-compose)
CMD ["/bin/bash", "/freqtrade/start.sh"]