# This file is used to build the docker image for the frontend
FROM python:3.10.8

#Set the working directory
WORKDIR /home

#Install the requirements
COPY requirements.txt .

#Upgrade pip
RUN pip install --upgrade pip

#Install the requirements
RUN pip install --no-cache-dir -r requirements.txt

#Copy the app.py file
COPY . .

#Expose port 8000
EXPOSE 8000

#Start the streamlit app
CMD ["uvicorn", "haystack_api:app", "--host 0.0.0.0", "--port 8000"]