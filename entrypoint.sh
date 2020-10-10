#!/bin/sh -l

cp /app/misspell.json /github/workflow/misspell.json
cp /app/schema_validator.json /github/workflow/schema_validator.json
echo "::add-matcher::${RUNNER_TEMP}/_github_workflow/misspell.json"
echo "::add-matcher::${RUNNER_TEMP}/_github_workflow/schema_validator.json"
echo "TERM: changing from $TERM -> xterm"
export TERM=xterm

echo Running: Spellcheck
/app/bin/misspell ./issues
exit_code=$?

if [ "$exit_code" = "0" ]; then
    echo "SpellCheck ok"
else
    echo "SpellCheck error"
fi

echo Running: Schema Validator
python /app/schema_validator.py
exit_code=$?

if [ "$exit_code" = "0" ]; then
    echo "Schema validated with no errors"
else
    echo "Schema has issues"
fi
