FROM python:3.9-slim
WORKDIR /backend
COPY . /backend/
RUN ls -lrt
##RUN pip install --upgrade pip
RUN pip install -r requirements.txt
EXPOSE 5001
CMD ["python", "backend.py"]