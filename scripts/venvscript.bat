
pip download -d packages wheel pip setuptools
pip download -d packages xlrd pylint pytest
pip download -d packages -r requirements.txt

python setup.py sdist
python -m venv venv
mkdir venv\packages\
copy packages\*.* venv\packages\
copy dist\*.tar.gz venv\packages\
cd venv\Scripts\
activate
pip install --no-index --find-links=..\packages\ wheel
python -m pip install --no-index --find-links=..\packages\ --upgrade pip setuptools
pip install --no-index --find-links=..\packages\ xlrd pylint pytest
pip install --no-index --find-links=..\packages\ -r requirements.txt
