FROM python:3
COPY . /app2
WORKDIR /app2
RUN pip install -r requirements.txt
EXPOSE 5001
ENTRYPOINT ["flask"]
CMD ["run", "--host=0.0.0.0", "--port=5001"]