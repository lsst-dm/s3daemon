VENVDIR = venv

venv:
	python -m venv $(VENVDIR)
	( \
		. $(VENVDIR)/bin/activate; \
		pip install -r ../requirements.txt; \
		pip install -r requirements.txt; \
	)

report: venv
	( \
		. $(VENVDIR)/bin/activate; \
		python report.py logs/*; \
	)

clean:
	rm -rf $(VENVDIR)
