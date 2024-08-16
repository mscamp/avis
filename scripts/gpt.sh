#!/bin/bash

# Variables
QUERY=$1
RESPONSE=$(tgpt -q "Rispondi in al massimo 100 parole: ${QUERY}")

# Response
espeak-ng -v roa/it "${RESPONSE}"