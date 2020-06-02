
#!/bin/bash

echo "Waiting database connection"
python3 databaseValidateConnection.py

echo "Applying database migrations"
python3 migrations/databaseMigration.py

echo "Starting application"
python3 worker.py
