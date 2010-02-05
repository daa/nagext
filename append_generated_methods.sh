#!/bin/sh

cat nagext.tmpl > nagext.py

./nag_external_commands.py >> nagext.py

