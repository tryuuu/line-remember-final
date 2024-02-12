#!/bin/bash
aws ecr get-login-password --region ap-northeast-1 | docker login --username AWS --password-stdin 361452760157.dkr.ecr.ap-northeast-1.amazonaws.com
docker build -t ryu-ocr-test --platform linux/x86_64 .
docker tag ryu-ocr-test:latest 361452760157.dkr.ecr.ap-northeast-1.amazonaws.com/ryu-ocr-test:latest
docker push 361452760157.dkr.ecr.ap-northeast-1.amazonaws.com/ryu-ocr-test:latest