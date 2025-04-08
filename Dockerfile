FROM nvidia/cuda:12.6.0-cudnn-devel-ubuntu22.04

# Update
ARG DEBIAN_FRONTEND=noninteractive
ENV TZ=Asia/Shanghai
RUN apt-get update && apt-get install -y \
    software-properties-common \
    wget \
    build-essential \
    libssl-dev \
    zlib1g-dev \
    libbz2-dev \
    libreadline-dev \
    libsqlite3-dev \
    curl \
    libncursesw5-dev \
    xz-utils \
    tk-dev \
    libxml2-dev \
    libxmlsec1-dev \
    libffi-dev \
    liblzma-dev \
    git

# Install Python 3.11
RUN apt-get update && \
    apt-get install -y python3.11 python3.11-venv python3.11-dev python3.11-distutils

# Set Python and pip
RUN ln -sf /usr/bin/python3.11 /usr/bin/python && \
    curl -sS https://bootstrap.pypa.io/get-pip.py | python


# Install PyTorch, TorchVision, and Torchaudio with CUDA 12.6 support
RUN pip install --no-cache-dir torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu126

# Install the Transformers library version 4.50.0
RUN pip install --no-cache-dir transformers==4.50.0

# Install Accelerate from the Hugging Face GitHub repository
RUN pip install --no-cache-dir git+https://github.com/huggingface/accelerate

# Copy the local evo2 folder to /evo2 in the container
COPY evo2 /evo2

# Configure Git to mark the directories as safe
RUN git config --global --add safe.directory /evo2 && \
    git config --global --add safe.directory /evo2/vortex

# Install the evo2 package
WORKDIR /evo2

RUN pip install --no-cache-dir .

# Install Transformer Engine for PyTorch version 1.13.0
RUN pip install --no-cache-dir "transformer_engine[pytorch]==1.13.0"


COPY app /app
WORKDIR /app
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]