# Makefile

.PHONY: install

OS := $(shell uname)

ifeq ($(OS),Linux)
    ACTIVATE_CMD = source venv/bin/activate
else ifeq ($(OS),Darwin)
    ACTIVATE_CMD = source venv/bin/activate
else ifeq ($(OS),FreeBSD)
    ACTIVATE_CMD = source venv/bin/activate
else ifeq ($(OS),Windows_NT)
    ACTIVATE_CMD = venv\Scripts\activate
else
    $(error Unsupported OS)
endif

# Install the package using pipx
install:
	@echo "Installing using pipx..."
	pipx install .
	@echo "Installation complete!"
