FROM python:3.6

COPY src/ /opt/retail_checkout

COPY data /tmp/data

WORKDIR /opt/retail_checkout

RUN pip install --no-cache-dir -r requirements.txt

RUN pip install .

ENTRYPOINT [ "gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "retail_app:app" ]