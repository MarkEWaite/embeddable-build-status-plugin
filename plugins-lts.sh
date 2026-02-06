#!/bin/bash

VERSION=2.541.1.35570
ENVELOPE=envelope-core-mm
[ ! -f temp.json ] && curl -L "https://jenkins-updates.cloudbees.com/update-center/$ENVELOPE/update-center.json?version=$VERSION" | sed -e '1d' -e '$d' > temp.json
jq '.envelope.plugins | to_entries | [.[]  | select(.value.tier=="verified"  ) | [.key, .value.name, .value.tier]]' temp.json 2>&1 | sed -e 's,Jenkins ,,g' -e 's,Pipeline:,Pipeline,g' -e 's, plugin,,g' -e 's, Plugin,,g' -e 's,Plugin ,,g' | tee verified.json
jq '.envelope.plugins | to_entries | [.[]  | select(.value.tier=="compatible") | [.key, .value.name, .value.tier]]' temp.json 2>&1 | sed -e 's,Jenkins ,,g' -e 's,Pipeline:,Pipeline,g' -e 's, Plugin,,g' -e 's,Plugin ,,g' | tee compatible.json
# use this if you need to generate a csv:
# jq -r '.envelope.plugins | to_entries | [.[] | [.key, .value.name, .value.tier, .value.version]][] | @csv' temp.json > "cap-plugin-list_${VERSION}_${ENVELOPE}.csv"
