"""Rebuild curated data. The functional HTML shell is maintained directly."""
from pathlib import Path
import subprocess,sys
root=Path(__file__).resolve().parent
subprocess.run([sys.executable,str(root/'scripts'/'build_data.py')],check=True)
print('App ready:',root/'index.html')
