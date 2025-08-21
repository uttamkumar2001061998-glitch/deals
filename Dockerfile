# Step 1: Use official Python image
FROM python:3.12-slim

# Step 2: Set working directory inside container
WORKDIR /app

# Step 3: Copy requirements.txt first
COPY requirements.txt .

# Step 4: Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Step 5: Copy the rest of your project
COPY . .

# Step 6: Expose Flask port
EXPOSE 5000

# Step 7: Run the Flask app
CMD ["python", "app.py"]
