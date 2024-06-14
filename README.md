# 1password-audit
[![CC BY-NC-SA 4.0][cc-by-nc-sa-shield]][cc-by-nc-sa] [![status: hibernate](https://github.com/GIScience/badges/raw/master/status/hibernate.svg)](https://github.com/GIScience/badges#hibernate)

This script is designed to audit your 1Password vault and ensure that all stored passwords adhere to predefined rules, providing a systematic approach to password management. By using 1Password's CLI, the script checks each password entry for compliance with specified criteria and alerts you if any entries do not meet these standards.

## Features
- Customizable Ideal Password Length: Set your desired password length (default is 64 characters).
- Ownership Tagging: Mark accounts with specific ownership tags to handle exceptions, like storing a friend's credentials in your vault.
- Max Length Field: Define a custom field name to specify maximum allowable password lengths.

## Dependencies
- [1Password's CLI](https://developer.1password.com/docs/cli)

## Usage
To run the script, use the following command:
```bash
python3 vault_password_auditor.py [ideal_password_length] [ownership_tag] [max_length_field_name]
```
- `ideal_password_length` (optional): Desired length for passwords. Default is 64.
- `ownership_tag` (optional): Tag for accounts that have specific ownership. Default is "Friend's account".
- `max_length_field_name` (optional): Field name used to specify the maximum allowable password length. Default is "Maximum length".

## License
This work is licensed under a
[Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License][cc-by-nc-sa].

[![CC BY-NC-SA 4.0][cc-by-nc-sa-image]][cc-by-nc-sa]

[cc-by-nc-sa]: http://creativecommons.org/licenses/by-nc-sa/4.0/
[cc-by-nc-sa-image]: https://licensebuttons.net/l/by-nc-sa/4.0/88x31.png
[cc-by-nc-sa-shield]: https://img.shields.io/badge/License-CC%20BY--NC--SA%204.0-lightgrey.svg
