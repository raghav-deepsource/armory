#!/bin/sh -l

cp /app/misspell.json /github/workflow/misspell.json
echo "::add-matcher::${RUNNER_TEMP}/_github_workflow/misspell.json"
echo "TERM: changing from $TERM -> xterm"
export TERM=xterm

IssueDir="${INPUT_ISSUES-PATH:-"./issues"}"

echo Running: Spellcheck
/app/bin/misspell "$IssueDir"
exit_code=$?

if [ "$exit_code" = "0" ]; then
    echo "SpellCheck ok"
else
    echo "SpellCheck error"
fi
