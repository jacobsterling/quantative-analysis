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

# Copy requirements.txt and install Python dependencies
COPY requirements.txt /freqtrade/
RUN pip install --no-cache-dir numpy cython
RUN pip install --no-cache-dir -r requirements.txt

# Clone Freqtrade repository
RUN git clone https://github.com/freqtrade/freqtrade.git /freqtrade

# Install Freqtrade
RUN pip install -e .

# Copy your custom files
COPY . /freqtrade/user_data/

# Expose port 8080 for the Freqtrade API
EXPOSE 8080

# Set the entrypoint
ENTRYPOINT ["freqtrade"]

# Default command (can be overridden)
CMD ["trade", "--config", "config.json"]