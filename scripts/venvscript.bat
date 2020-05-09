pip download -d packages pip setuptools
pip download -d packages -r requirements.txt

python setup.py sdist
python -m venv venv
mkdir venv\packages\
copy packages\*.tar.gz venv\packages\
copy packages\*.whl venv\packages\
copy dist\*.tar.gz venv\packages\
cd venv\Scripts\
activate
python -m pip install --no-index --find-links=..\packages\ --upgrade pip setuptools
pip install --no-index --find-links=..\packages\ ..\packages\plsql2postgre-0.1.0.tar.gz
