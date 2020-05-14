del /q packages
pip download -d packages wheel pip setuptools
pip download -d packages xlrd pylint pytest pytest-cov
pip download -d packages -r requirements.txt
