# Evo2 docker deployment

## Overview
Evo 2 is a state of the art DNA language model for long context modeling and design. This repository provides a Docker container for easy deployment of the Evo2 model.

> Note: To run on GPUs with compute capability less than 8.9, `use_fp8_input_projections` is set to `False`. This may have an impact on the performance of the model.

## Prerequisites
- Docker installed
- NVIDIA Container Toolkit installed
- NVIDIA GPU with CUDA support (like RTX 3090, A100, etc.)

## Build docker image
```bash
docker build --platform=linux/amd64 -t evo2:latest .
# or
docker build --platform=linux/amd64 -t evo2:latest -f ./Dockerfile.cuda121 .
```

## Run docker container

```bash
docker run -itd --runtime=nvidia --gpus all --name evo2 -v /evo2/model/weights/dir/path/evo2_7b:/evo2/evo2_7b -p 8000:8000 evo2
```

Or you can pull the image from Docker Hub:

```bash
```

## API Usage

### 1. Generation
```bash
 curl -X POST -H "Authorization: Bearer 581e45f1-bb33-4c49-8727-499fe2dd3c51" -H "Content-Type: application/json" -d '{"prompt_seqs": ["GACACCATCGAATGGCGCAAAACCTTTCGC"], "n_tokens": 500, "temperature": 1.0, "top_k": 4, "top_p": 1.0}' http://localhost:8000/evo2_7b/generate
```

### 2. Scoring

```bash
curl -X POST -H "Authorization: Bearer 581e45f1-bb33-4c49-8727-499fe2dd3c51" -H "Content-Type: application/json" -d '{"seqs": ["GACACCATCGAATGGCGCAAAACCTTTCGCGGTATGGCATGATAGCGCCCGGAAGAGAGTCAATTCAGGGTGGTGAATGTGAAACCAGTAACGTTATACGATGTCGCAGAGTATGCCGGTGTCTCTTATCAGACCGTTTCCCGCGTGGTGAACCAGGCCAGCC"], "batch_size": 1}' http://localhost:8000/evo2_7b/scoring
```

## Acknowledgements

This repository is based on the [Evo2](https://github.com/biowayai/evo2) repository. The original project is licensed under the [Apache License 2.0](https://www.apache.org/licenses/LICENSE-2.0).