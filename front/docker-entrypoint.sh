
#!/bin/bash

echo "Waiting database connection"
python3 databaseValidateConnection.py

echo "Starting application"
python3 front.py