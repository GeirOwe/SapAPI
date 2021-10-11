FROM python:3.8-alpine

WORKDIR /sapapi

#the following command is to fix an issue with pandas in docker alpine
RUN apk add --update curl gcc g++ \
    && rm -rf /var/cache/apk/*
RUN ln -s /usr/include/locale.h /usr/include/xlocale.h

COPY requirements.txt requirements.txt

RUN apk add --no-cache gcc musl-dev libffi-dev openssl-dev python3-dev
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN pip install requests
RUN pip install --no-cache-dir pandas

# Copy the files you have created earlier into our image 
# for the app to run
COPY main.py .
COPY config.py .
COPY app/*.py app/
COPY app/templates/*.html app/templates/

# Establish the runtime user (with no password and no sudo)
RUN useradd -u 1001 sapuser && chown -R sapuser /sapapi
USER sapuser
# Adds permission for appuser (non-root) to access the /flask folder
RUN chown -R sapuser /flask_session

# the flask app to be run
ENV FLASK_APP main.py

EXPOSE 5000
CMD ["flask", "run", "--host=0.0.0.0"]
