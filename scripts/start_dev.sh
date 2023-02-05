#!/usr/bin/env bash
python manage.py recreate_db
python manage.py run_dev_server
