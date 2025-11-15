#!/usr/bin/env python3
"""
Create a virtualenv and install requirements.

Usage:
  python setup_env.py                         # uses ./venv and ./requirements.txt
  python setup_env.py --venv /path/to/venv
  python setup_env.py --req requirements.txt --dev requirements_dev.txt
  python setup_env.py --python python3.10     # choose a python binary
"""
import argparse
import shutil
import subprocess
import sys
from pathlib import Path

def run(cmd, **kwargs):
    print("+", " ".join(cmd))
    subprocess.run(cmd, check=True, **kwargs)

def get_pip_path(venv_path: Path) -> Path:
    if sys.platform == "win32":
        return venv_path / "Scripts" / "pip.exe"
    return venv_path / "bin" / "pip"

def main():
    parser = argparse.ArgumentParser(description="Create a venv and install requirements.")
    parser.add_argument("--venv", "-v", type=Path, default=Path.cwd() / "venv",
                        help="Path to virtual environment (default: ./venv)")
    parser.add_argument("--req", type=Path, default=Path.cwd() / "requirements.txt",
                        help="Path to requirements file (default: ./requirements.txt)")
    parser.add_argument("--dev", type=Path, default=None,
                        help="Optional dev requirements file (e.g. requirements_dev.txt)")
    parser.add_argument("--python", type=str, default=sys.executable,
                        help="Python interpreter to create the venv (default: current interpreter)")
    args = parser.parse_args()

    venv_path: Path = args.venv.resolve()
    req_file: Path = args.req.resolve()
    dev_file: Path | None = args.dev.resolve() if args.dev else None
    python_exe: str = args.python

    if not req_file.exists():
        print(f"Error: requirements file not found: {req_file}")
        sys.exit(2)

    # Create venv
    print(f"Creating virtualenv at: {venv_path} using python: {python_exe}")
    try:
        run([python_exe, "-m", "venv", str(venv_path)])
    except subprocess.CalledProcessError as e:
        print("Failed to create virtualenv:", e)
        sys.exit(3)

    pip_path = get_pip_path(venv_path)
    if not pip_path.exists():
        print(f"Error: pip not found in venv at {pip_path}")
        sys.exit(4)

    # Upgrade pip/setuptools/wheel first
    try:
        run([str(pip_path), "install", "--upgrade", "pip", "setuptools", "wheel"])
    except subprocess.CalledProcessError as e:
        print("Failed to upgrade pip/setuptools/wheel:", e)
        sys.exit(5)

    # Install requirements
    try:
        run([str(pip_path), "install", "--no-cache-dir", "-r", str(req_file)])
        if dev_file and dev_file.exists():
            run([str(pip_path), "install", "--no-cache-dir", "-r", str(dev_file)])
    except subprocess.CalledProcessError as e:
        print("pip install failed:", e)
        print("If install fails for packages that require system libraries (e.g. mysqlclient),")
        print("make sure the corresponding OS packages are installed (libmysqlclient-dev, libpq-dev, build-essential, python3-dev, etc.)")
        sys.exit(6)

    print("Virtualenv created and requirements installed successfully.")
    print("Activate it (bash):")
    if sys.platform == "win32":
        print(f"  {venv_path}\\Scripts\\activate")
    else:
        print(f"  source {venv_path}/bin/activate")

if __name__ == "__main__":
    main()