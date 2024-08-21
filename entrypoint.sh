#!/bin/bash

# Start Marqo container
docker run --name marqo -d -p 8882:8882 marqoai/marqo

# Wait for Marqo to start
sleep 300

# Activate virtual environment
source venv/bin/activate

# Index the data
python3 index_data.py

# Start the application
python3 app.py
