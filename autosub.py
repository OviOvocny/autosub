#!/usr/bin/env python3

import argparse
import os, sys
import requests
import json
import re

# ARGS
ap = argparse.ArgumentParser(description="Translate .ass subtitle dialogue lines")
# positional
ap.add_argument("input", help="input file path")
ap.add_argument("output", default=None, nargs="?", help="output file path (created if doesn't exist, stdout by default)")
# required
required = ap.add_argument_group('required arguments')
required.add_argument("-l", "--languages", help="source and target languages in format source:target with codes (for example en:de)", required=True)
# optional
ap.add_argument("-s", "--stream", action="store_true", help="stream (uses less memory, takes longer)")
ap.add_argument("-v", "--verbose", action="store_true", help="print status messages (only if output is not stdout)")
ap.add_argument("--key", help="Translator API key, if not set as environment variable", default=None)

args = ap.parse_args()

# KEY
if 'TRANSLATOR_KEY' in os.environ:
    skey = os.environ['TRANSLATOR_KEY']
elif args.key is not None:
    skey = args.key
else:
    print('No key provided. Environment variable TRANSLATOR_KEY is not set in this environment. Use -h for help.', file=sys.stderr)
    exit(10)

# TL SETUP
base = 'https://api.cognitive.microsofttranslator.com'
path = '/translate?api-version=3.0'
langs = args.languages.split(":")
params = f'&from={langs[0]}&to={langs[1]}'
url = base + path + params
headers = {
    'Ocp-Apim-Subscription-Key': skey,
    'Content-type': 'application/json'
}

# FILE SETUP
try:
  ifile = open(args.input, "r")
except FileNotFoundError:
  print(f"Cannot open input file {args.input}", file=sys.stderr)
  exit(11)

if args.output == "stdout":
  args.output = None

try:
  ofile = open(args.output, "w+")
except TypeError:
  ofile = sys.stdout
except FileNotFoundError:
  print(f"Cannot open output file {args.output}", file=sys.stderr)
  ifile.close()
  exit(12)

# HELPERS
def translate (lines):
  if len(lines) == 0:
    return []
  body = list(map(lambda l: {"text": l}, lines))
  req = requests.post(url, headers=headers, json=body)
  res = req.json()
  if not req.ok:
    ifile.close()
    ofile.close()
    print(f"API error: {res['error']['message']}", file=sys.stderr)
    exit(20)
  return list(map(lambda l: l["translations"][0]["text"], res))

def get_dialogue (line):
  dialogue = ",".join(line.split(",")[9:]).rstrip("\n")
  return re.sub(r"\{.*?\}", "", dialogue)

def vprint (text):
  if args.verbose and args.output != None:
    print(text)

linebuf = []
tl_buf = []
bufsize = 0
completed = []

vprint(f"Starting file parsing in {'stream' if args.stream else 'buffer'} mode")
for line in ifile:
  if line.startswith("Dialogue:"):
    line = line.replace("\\N", " ")
    dialogue = get_dialogue(line)
    if (args.stream):
      # stream mode, translate right now
      line = line.replace(dialogue, translate([dialogue])[0])
      ofile.write(line)
    else:
      # buffer mode, translate as much as possible later
      linebuf.append(line)
      if len(tl_buf) < 100 and bufsize + len(dialogue) < 5000:
        bufsize += len(dialogue)
        tl_buf.append(dialogue)
      else:
        vprint("Translating batch of lines")
        completed += translate(tl_buf)
        tl_buf = [dialogue]
        bufsize = len(dialogue)
  # not a dialogue line, copy over
  else:
    ofile.write(line)

if not args.stream:
  vprint("Translating batch of lines")
  completed += translate(tl_buf)
  vprint("Writing buffered translations to output")
  for line, translation in zip(linebuf, completed):
    dialogue = get_dialogue(line)
    line = line.replace(dialogue, translation)
    ofile.write(line)

# EXITING
vprint("Finished!")
ifile.close()
ofile.close()