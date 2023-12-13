FROM public.ecr.aws/lambda/python:3.10

COPY requirements.txt  .
RUN  pip3 install -r requirements.txt --target "${LAMBDA_TASK_ROOT}"

COPY app.py ${LAMBDA_TASK_ROOT}
COPY src/ ${LAMBDA_TASK_ROOT}/src/
ENV LINE_CHANNEL_ACCESS_TOKEN ""
ENV DYNAMODB_TABLE_NAME "line-knowledge-db"
ENV DYNAMODB_TABLE_NAME2 "line-knowledge-db2"
CMD [ "app.handler" ]
