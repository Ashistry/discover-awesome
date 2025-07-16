# Makefile

.PHONY: install

# Install the package using pipx
install:
	@echo "Installing using pipx..."
	pipx install .
	@echo "Installation complete!"
