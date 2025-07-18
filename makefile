# Makefile

.PHONY: install

# Install the package using pipx
install:
	@echo "Installing using pipx..."
	python setup.py sdist bdist_wheel
	pipx install dist/discover_awesome-0.0.0-py3-none-any.whl 

uninstall:
	@echo "Uninstalling using pipx..."
	pipx uninstall discover-awesome

