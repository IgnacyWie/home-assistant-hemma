#!/bin/sh
# Report home/not_home for one MAC without exposing it in Home Assistant YAML.
set -eu

mac_file=${1:?MAC file path required}
[ -r "$mac_file" ] || exit 2

target=$(
  tr '[:lower:]' '[:upper:]' < "$mac_file" |
    tr -d ':-' |
    tr -d '[:space:]'
)

case "$target" in
  ''|*[!0-9A-F]*) exit 2 ;;
esac
[ "${#target}" -eq 12 ] || exit 2

scan=$(nmap -n -sn -PR -T4 --min-rate 10 --host-timeout 5s 192.168.1.0/24 2>/dev/null) || exit 3

if printf '%s\n' "$scan" |
  awk '/MAC Address:/{gsub(/[:-]/, "", $3); print toupper($3)}' |
  grep -qx "$target"
then
  printf 'home\n'
else
  printf 'not_home\n'
fi
