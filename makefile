lint:
	flake8 ycurve/ 
	mypy ycurve/
	pylint --rcfile .pylint.rc ycurve/