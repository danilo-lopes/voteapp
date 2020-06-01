#!/bin/bash
echo "Migration"
python3 migrations/setup.py
sleep 2

echo "Startuping Application"
python3 voting.py
