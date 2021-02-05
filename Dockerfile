FROM python:3.8-alpine

WORKDIR /sapapi

RUN apk add --update curl gcc g++ \
    && rm -rf /var/cache/apk/*
RUN ln -s /usr/include/locale.h /usr/include/xlocale.h

COPY requirements.txt requirements.txt

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

ENV FLASK_APP main.py

EXPOSE 5000
CMD ["flask", "run", "--host=0.0.0.0"]
