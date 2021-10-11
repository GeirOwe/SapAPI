# pull official base image
FROM python:3.9.5-slim-buster

# create the app user
RUN addgroup --system app && adduser --system --group app
#RUN addgroup --system --group 101 app 
#RUN adduser --system --user 101 --group app app 

# create the appropriate directories
ENV APP_HOME=/sapapi
WORKDIR $APP_HOME

RUN pip install --upgrade pip
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
RUN pip install requests
RUN pip install --no-cache-dir pandas

# Copy the files you have created earlier into our image 
# for the app to run
COPY main.py .
COPY config.py .
COPY app/*.py app/
COPY app/templates/*.html app/templates/

# chown all the files to the user
RUN chown -R app:app $APP_HOME

# change to the app user
USER 101

# the flask app to be run
ENV FLASK_APP main.py

EXPOSE 5000
CMD ["flask", "run", "--host=0.0.0.0"]
