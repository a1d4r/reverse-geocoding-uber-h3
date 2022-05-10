# Thesis project

Scalable and efficient approach for reverse geocoding using Uber H3

## Setup

1. Clone this repository

```bash
git clone https://github.com/a1d4r/reverse-geocoding-uber-h3.git
cd reverse-geocoding-uber-h3 
```

2. If you don't have `Poetry` installed run:

```bash
make poetry-download
```

3. Install dependencies:
```bash
make install
```

## Development

Install pre-commit hooks:

```bash
make pre-commit-install
```

Format source code:

```bash
make format
```

Check codestyle and run static linters:

```bash
make lint
```

Run tests:

```bash
make test
```

Or everything in one command:
```
make format lint test
```


### Advanced Makefile usage

[`Makefile`](https://github.com/a1d4r/thesis-project/blob/master/Makefile) contains a lot of functions for faster development.

<details>
<summary>1. Download and remove Poetry</summary>
<p>

To download and install Poetry run:

```bash
make poetry-download
```

To uninstall

```bash
make poetry-remove
```

</p>
</details>

<details>
<summary>2. Install all dependencies and pre-commit hooks</summary>
<p>

Install requirements:

```bash
make install
```

Pre-commit hooks coulb be installed after `git init` via

```bash
make pre-commit-install
```

</p>
</details>

<details>
<summary>3. Codestyle</summary>
<p>

Automatic formatting uses `pyupgrade`, `isort` and `black`.

```bash
make codestyle

# or use synonym
make format
```

Codestyle checks only, without rewriting files:

```bash
make check-codestyle
```

> Note: `check-codestyle` uses `isort`, `black` and `darglint` library

Update all dev libraries to the latest version using one comand

```bash
make update-dev-deps
```
</p>
</details>

<details>
<summary>4. Code security</summary>
<p>

```bash
make check-security
```

This command identifies security issues with `Safety` and `Bandit`.

```bash
make check-security
```

To validate `pyproject.toml` use
```bash
make check-poetry
```

</p>
</details>


<details>
<summary>5. Linting and type checks</summary>
<p>

Run static linting with `pylint` and `mypy`:

```bash
make static-lint
```

</p>
</details>

<details>
<summary>6. Tests</summary>
<p>

Run `pytest`

```bash
make test
```

</p>
</details>

<details>
<summary>7. All linters</summary>
<p>

Of course there is a command to ~~rule~~ run all linters in one:

```bash
make lint
```

the same as:

```bash
make format lint test
```

</p>
</details>

<details>
<summary>8. Cleanup</summary>
<p>
Delete pycache files

```bash
make pycache-remove
```

Remove package build

```bash
make build-remove
```

Delete .DS_STORE files

```bash
make dsstore-remove
```

Remove .mypycache

```bash
make mypycache-remove
```

Or to remove all above run:

```bash
make cleanup
```

</p>
</details>

## 🛡 License

[![License](https://img.shields.io/github/license/a1d4r/thesis-project)](https://github.com/a1d4r/thesis-project/blob/master/LICENSE)

This project is licensed under the terms of the `MIT` license. See [LICENSE](https://github.com/a1d4r/thesis-project/blob/master/LICENSE) for more details.

## 📃 Citation

```bibtex
@misc{geocoding,
  author = {a1d4r},
  title = {Reverse geocoding algorithm based on Uber H3},
  year = {2022},
  publisher = {GitHub},
  journal = {GitHub repository},
  howpublished = {\url{https://github.com/a1d4r/thesis-project}}
}
```

## Credits [![🚀 Your next Python package needs a bleeding-edge project structure.](https://img.shields.io/badge/python--package--template-%F0%9F%9A%80-brightgreen)](https://github.com/TezRomacH/python-package-template)

This project was generated with [`python-package-template`](https://github.com/TezRomacH/python-package-template)
