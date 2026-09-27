#!/bin/bash
# Quick runner for BLIP-base on Colab (CPU)
# Usage: ./scripts/caption_blip_base.sh  (assumes colab session karhutla-cpu exists)
set -e
colab exec -s karhutla-cpu -f scripts/caption_assets.py 2>&1 | tail -20
