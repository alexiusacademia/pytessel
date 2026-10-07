#!/bin/sh
# Runs every tests/*.py with Adder and compares what it prints with
# tests/<name>.expected (what CPython prints for the same program).
#
#   tests/run.sh             run the tests
#   tests/run.sh --update    write the .expected files again, with python3
#
# Build Adder first: `tessel build . -o adder` in the project's folder.
cd "$(dirname "$0")" || exit 1
adder=../adder
[ -x "$adder" ] || { echo "build Adder first: tessel build . -o adder"; exit 1; }
failed=0
for test in *.py; do
    name="${test%.py}"
    # (helper.py is imported by modules.py; it isn't a test.)
    [ "$name" = helper ] && continue
    if [ "$1" = --update ]; then
        python3 "$test" > "$name.expected" 2>&1
        continue
    fi
    if "$adder" "$test" 2>&1 | diff "$name.expected" - > /dev/null; then
        echo "ok    $name"
    else
        echo "FAIL  $name"
        "$adder" "$test" 2>&1 | diff "$name.expected" - | head -10
        failed=1
    fi
done
exit $failed
