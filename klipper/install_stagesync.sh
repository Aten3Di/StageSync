#!/bin/bash

# Percorso del file da spostare
FILE="stagesync.py"

# Directory di destinazione
DEST_DIR="$HOME/klipper/klippy/extras"

# Verifica se il file esiste
if [ -f "$FILE" ]; then
    # Sposta il file nella directory di destinazione
    mv "$FILE" "$DEST_DIR"
    echo "Il file $FILE è stato spostato in $DEST_DIR."
else
    echo "Errore: il file $FILE non esiste nella directory corrente."
fi
