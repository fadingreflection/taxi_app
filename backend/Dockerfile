FROM python:3.10       

WORKDIR /backend

RUN pip install fastapi uvicorn

RUN pip install -U setuptools

COPY ./requirements.txt ./

RUN pip install -r requirements.txt --ignore-installed

COPY . .

EXPOSE 8080

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080" ,"--reload"]