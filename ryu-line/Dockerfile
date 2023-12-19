FROM public.ecr.aws/lambda/python:3.10

COPY requirements.txt  .
RUN  pip3 install -r requirements.txt --target "${LAMBDA_TASK_ROOT}"

COPY app.py ${LAMBDA_TASK_ROOT}
COPY src/ ${LAMBDA_TASK_ROOT}/src/
ENV LINE_CHANNEL_ACCESS_TOKEN "wmHVlXxcJNoUA7yk0D5F2Zljx4jesyUN/R82MWx2vlEEJ9SnmbS0SIUHDt32jVsZKEwtA9t7iyIC9DxkDmyMO8Vi1A4ROWYDq7STOrHwOzB1oo2nvRI/68XkT++ibGxnkHc4saWq84O8No3oO4XvyAdB04t89/1O/w1cDnyilFU="
ENV DYNAMODB_TABLE_NAME "line-knowledge-db"
ENV DYNAMODB_TABLE_NAME2 "line-knowledge-db2"
CMD [ "app.handler" ]
