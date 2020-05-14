@echo Start continues intergration of project "plsql2postgre"......

@set pyok=1
@set pset=nothing
@set pver=0.0.0
@for /f "tokens=1,2" %%v in ('python --version') do @set pset=%%v& @set pver=%%w
@if not "%pset%"=="Python" (@set pyok=0) else if "%pver%" lss "3.6.0" @set pyok=0
@if %pyok% equ 0 (@echo Install python v3.6.3......)&(@start /wait packages\python-3.6.3-amd64.exe /qn)

@echo Python is installed. Now upgrade pip and setuptools......
rem @pip install wheel >nul
rem @python -m pip install --upgrade pip setuptools >nul

@echo Create virtual environment......
@python -m venv venv
@mkdir venv\packages
@xcopy packages\*.* venv\packages /s >nul
@mkdir venv\plsql2postgre
@xcopy plsql2postgre\*.* venv\plsql2postgre /s >nul
@mkdir venv\tests
@xcopy tests\*.* venv\tests /s >nul
@copy .coveragerc venv\ >nul
@copy .pylintrc venv\ >nul
@copy requirements.txt venv\ >nul
@copy setup.py venv\ >nul

@echo Install dependencies in virtual environment......
@cd venv
@call Scripts\activate.bat
@pip install --no-index --find-links=packages\ wheel >nul
@python -m pip install --no-index --find-links=packages\ --upgrade pip setuptools >nul
@pip install --no-index --find-links=packages\ xlrd pylint pytest pytest-cov >nul
@pip install --no-index --find-links=packages\ -r requirements.txt >nul

@echo Run linting in virtual environment......
@pylint plsql2postgre

@echo Run testing in virtual environment......
@pytest --cov=plsql2postgre --cov-report term-missing tests

@echo Clean up virtual environment......
@call Scripts\deactivate.bat
@cd ..\
@rmdir /s /q venv

@echo Continues intergration of project "plsql2postgre" is ended.
