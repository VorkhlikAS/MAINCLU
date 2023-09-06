#!/bin/bash

python3 ./db/main.py

uvicorn server:app --reload --host 0.0.0.0