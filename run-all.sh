#!/bin/sh

echo "Running sample phase..."
../run.sh sample

echo "Running test phase..."
../run.sh test

echo "Running submit phase..."
../run.sh submit
