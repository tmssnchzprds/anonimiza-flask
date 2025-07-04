FROM mcr.microsoft.com/azure-cli-python:3.9
WORKDIR /app
COPY . /app
RUN pip install -r requirements.txt
RUN chmod +x startup.sh
CMD ["./startup.sh"]
