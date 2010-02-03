#!/bin/sh

cat nagext.tmpl > nagext.tmp

./nag_external_commands.py >> nagext.tmp

sed 's/\t/    /g' nagext.tmp | ./wrap_rest.py 120 --python | sed 's/    /\t/g' > nagext.py

rm nagext.tmp

