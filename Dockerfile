# Python 3.9 slim image එක භාවිතා කරන්න
FROM python:3.9-slim

# වැඩ කරන directory එක set කරන්න
WORKDIR /app

# requirements.txt එක copy කරගන්න
COPY requirements.txt .

# pip මගින් dependencies install කරන්න
RUN pip install --no-cache-dir -r requirements.txt

# project එකේ සියලු files copy කරගන්න
COPY . .

# port 8000 expose කරයි (health check සදහා)
EXPOSE 8000

# main.py file එක run කරන command එක
CMD ["python", "main.py"]
