#!/bin/sh

cat nagext.tmpl.py > nagext.py

./nag_external_commands.py >> nagext.py

