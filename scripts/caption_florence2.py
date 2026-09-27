#!/usr/bin/env python3
# Thin wrapper for colab exec convenience — calls caption_assets.py with florence2
import subprocess, sys
sys.exit(subprocess.call([sys.executable, "scripts/caption_assets.py", "--model", "florence2", "--zip", "/content/karhutla-assets.zip"] + sys.argv[1:]))
