# 1password-audit
[![CC BY-NC-SA 4.0][cc-by-nc-sa-shield]][cc-by-nc-sa] [![status: hibernate](https://github.com/GIScience/badges/raw/master/status/hibernate.svg)](https://github.com/GIScience/badges#hibernate)

I really like having a systematical approach when it comes to storing my passwords. It gives me a sense of order, if my passwords adhere to predifined rules, and this is a script to audit a vault to ensure it adheres to them.

Using [1Password's CLI](https://developer.1password.com/docs/cli), this script will audit your passwords for the specified rules and alert you, if there are entries that do not align with them.

## Usage
```python
python3 1password-audit.py
```

## Dependencies
- [1Password's CLI](https://developer.1password.com/docs/cli)

## License
This work is licensed under a
[Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License][cc-by-nc-sa].

[![CC BY-NC-SA 4.0][cc-by-nc-sa-image]][cc-by-nc-sa]

[cc-by-nc-sa]: http://creativecommons.org/licenses/by-nc-sa/4.0/
[cc-by-nc-sa-image]: https://licensebuttons.net/l/by-nc-sa/4.0/88x31.png
[cc-by-nc-sa-shield]: https://img.shields.io/badge/License-CC%20BY--NC--SA%204.0-lightgrey.svg
