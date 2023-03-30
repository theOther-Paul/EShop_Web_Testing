SET dt=%DATE:~-4%.%DATE:~4,2%.%DATE:~7,2%_%TIME:~0,2%.%TIME:~3,2%.%TIME:~6,2%
SET dt=%dt: =0%
SET file_name="Pytest Report at "
SET complete_name=%file_name%%dt%
venv\Scripts\python -m pytest --html=test_reports/%file_name%%dt%.html --self-contained-html tests.py