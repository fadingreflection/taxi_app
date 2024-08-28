FROM python:3.10      

WORKDIR /frontend

RUN pip install fastapi uvicorn setuptools 

COPY requirements.txt ./

RUN pip install -r requirements.txt --ignore-installed

COPY . .

# COPY ./.streamlit ./frontend/.streamlit

# COPY ./pages ./frontend/pages

# COPY Hello.py ./

# COPY taxi_logo.png ./

EXPOSE 8501

CMD ["streamlit", "run", "Hello.py"]