FROM python:3.10-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    gdal-bin \
    libgdal-dev \
    g++ \
    && rm -rf /var/lib/apt/lists/*

ENV CPLUS_INCLUDE_PATH=/usr/include/gdal
ENV C_INCLUDE_PATH=/usr/include/gdal

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY watershed_dashboard.py .
COPY shapefile_utils.py .
COPY create_sample_data.py .

RUN mkdir -p /app/data /app/sample_data

EXPOSE 8501

HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health || exit 1

CMD ["streamlit", "run", "watershed_dashboard.py", "--server.port=8501", "--server.address=0.0.0.0"]
