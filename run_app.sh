#!/bin/bash

# Navigate to the directory where this script is located
cd "$(dirname "$0")"

# Set environment variables
export FLASK_APP=app.main
export FLASK_ENV=development

export FLASK_RUN_PORT=5099

# Optionally, set the host
# export FLASK_RUN_HOST=0.0.0.0  # Uncomment this line to bind to all network interfaces

# Activate your virtual environment if needed
if [ -d .myenv ]; then
    source .myenv/bin/activate
fi

# Run Flask application
flask run
