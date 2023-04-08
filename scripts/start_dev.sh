#!/usr/bin/env bash
flask --app manage:app recreate_db
flask --app manage:app --debug run --host=0.0.0.0
