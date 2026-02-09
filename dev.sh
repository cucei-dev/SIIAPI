#!/bin/bash
rm db.sqlite3
fastapi dev app/main.py
