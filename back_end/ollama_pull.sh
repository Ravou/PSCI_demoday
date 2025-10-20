#!/bin/bash

while true; do
  echo "Tentative de téléchargement de l’image Ollama..."
  docker pull ollama/ollama:latest && break
  echo "Échec du téléchargement. Nouvelle tentative dans 15 secondes..."
  sleep 15
done
