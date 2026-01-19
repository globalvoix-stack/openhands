#!/bin/bash
# This hook was installed by Thinksoft
# It calls the pre-commit script in the .thinksoft directory

if [ -x ".thinksoft/pre-commit.sh" ]; then
    source ".thinksoft/pre-commit.sh"
    exit $?
else
    echo "Warning: .thinksoft/pre-commit.sh not found or not executable"
    exit 0
fi
