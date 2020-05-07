FROM ubuntu:18.04

RUN apt update -y && \
    apt install -y python3-pip python3

RUN mkdir -p /api

COPY requirements.txt /api

WORKDIR /api

RUN pip3 install -r requirements.txt

# Install deps + add Chrome Stable + purge all the things
RUN apt-get update && apt-get install -y \
  apt-transport-https \
  ca-certificates \
  curl \
  gnupg \
  --no-install-recommends \
  && curl -sSL https://deb.nodesource.com/setup_12.x | bash - \
  && curl -sSL https://dl.google.com/linux/linux_signing_key.pub | apt-key add - \
  && echo "deb https://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google-chrome.list \
  && apt-get update && apt-get install -y \
  google-chrome-stable \
  fontconfig \
  fonts-ipafont-gothic \
  fonts-wqy-zenhei \
  fonts-thai-tlwg \
  fonts-kacst \
  fonts-symbola \
  fonts-noto \
  fonts-freefont-ttf \
  nodejs \
  --no-install-recommends \
  && apt-get purge --auto-remove -y curl gnupg \
  && rm -rf /var/lib/apt/lists/*

ARG CACHEBUST=1
RUN npm install -g lighthouse@next

# Add Chrome as a user
RUN groupadd -r chrome && useradd -r -g chrome -G audio,video chrome \
  && mkdir -p /home/chrome/reports && chown -R chrome:chrome /home/chrome

# Run Chrome non-privileged
USER chrome

# CMD ["lighthouse", "http://18.222.118.221", "--output" ,"json", "--chrome-flags='--headless --disable-gpu --no-sandbox']

COPY api.py /api/api.py

ENTRYPOINT ["flask"]
CMD ["run", "--host=0.0.0.0", "--port=9000"]