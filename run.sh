#!/bin/sh

SCRIPT="./solution.py"

# One of 'sample', 'test' or 'submit'
phase="${1:?Specify run phase (sample, test or submit)}"

"$SCRIPT" < "${phase}Input" > "${phase}Output"
