FROM python:3-slim
WORKDIR /usr/src/app
COPY http.reqs.txt ./
RUN python -m pip install --no-cache-dir -r http.reqs.txt
COPY ./notification_manager_1.py ./amqp_setup.py ./
CMD [ "python", "./notification_manager_1.py" ]