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
#COPY .env .
COPY app/*.py app/
COPY app/templates/*.html app/templates/

#Add a new user "gow" with user id 6866
#RUN useradd -u 6866 gow
#Change to non-root privilege
#USER gow

ENV FLASK_APP main.py

EXPOSE 5000
CMD ["flask", "run", "--host=0.0.0.0"]
