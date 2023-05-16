# 👥 Contributing Guide

I appreciate your interest in contributing to the project! This document outlines how to contribute to the project, including the contribution process, code style, and testing.

## 🔄️ Contribution process

To contribute, please follow these steps:

1. Fork the project repository on GitHub.
1. Create a new branch for your feature or bug fix.
1. Setup development environment.

    ```shell
    # install pipx
    python3 -m pip install --user pipx
    pipx ensurepath

    # install poetry + plugins
    pipx install poetry
    pipx inject poetry poetry-plugin-up
    pipx inject poetry poetry-dynamic-versioning
    pipx inject poetry poethepoet

    # install project dependencies
    poetry install

    # bump dependencies to the latest
    poetry up --latest

    # do test build
    poetry build
    ```

1. Make your changes.
1. Lint and validate your code.

    ```shell
    poetry run pre-commit run --all-files
    ```

1. Commit your changes.
1. Make sure the `README.md` and any other relevant documentation are kept up-to-date.
1. Make your changes and commit them with descriptive commit messages; check [Conventional Commits](https://www.conventionalcommits.org) as a suggestion.
1. Push to your forked repository.
1. Create a new pull request from your fork to this project.
1. Please ensure that your pull request includes a detailed description of your changes and that your code adheres to the code style guidelines outlined below.

## 🔰 Code of Conduct

All contributors are expected to adhere to the project name code of conduct. Therefore, please review it before contributing [`Code of Conduct`](./CODE_OF_CONDUCT.md).

## 📄 License

By contributing to this project, you agree that your contributions will be licensed under the project license.

Thank you for contributing!
