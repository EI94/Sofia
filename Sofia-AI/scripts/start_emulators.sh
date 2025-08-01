#!/usr/bin/env bash
set -e
export FIRESTORE_EMULATOR_HOST=localhost:8080
gcloud beta emulators firestore start --host-port=8080 \
        --project test-sofia &>/tmp/emu_fs.log &
echo "Firestore emulator up → $FIRESTORE_EMULATOR_HOST"
