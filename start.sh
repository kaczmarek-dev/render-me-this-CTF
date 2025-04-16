#!/bin/bash

exec python3 config_set_prefix.py $PREFIX &
exec python3 main.py &
exec python3 admin_bot.py
