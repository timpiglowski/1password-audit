import json
import subprocess
import sys
import time

# Define the default ideal password length, ownership tag, and maximum length field name
IDEAL_PASSWORD_LENGTH = 64
OWNERSHIP_TAG = "Fremdaccount"
MAX_LENGTH_FIELD_NAME = "Maximallänge"

# Parse command-line arguments
if len(sys.argv) > 1:
    try:
        IDEAL_PASSWORD_LENGTH = int(sys.argv[1])
    except ValueError:
        print("Invalid input for ideal password length. Using default value of 64.")
    if len(sys.argv) > 2:
        OWNERSHIP_TAG = sys.argv[2]
    if len(sys.argv) > 3:
        MAX_LENGTH_FIELD_NAME = sys.argv[3]

def print_green(text):
    print(f"\033[0;32m{text}\033[0m")

def print_yellow(text):
    print(f"\033[0;33m{text}\033[0m")

def print_red(text):
    print(f"\033[0;31m{text}\033[0m")

class VaultItem:
    def __init__(self, item_id, title, category, tags):
        self.item_id = item_id
        self.title = title
        self.category = category
        self.tags = tags
        self.password = None
        self.max_length = None
        self.failed_tests = []

    def fetch_details(self):
        try:
            result = subprocess.run(['op', 'item', 'get', self.item_id, '--format', 'json'], capture_output=True, text=True, check=True)
            item_details = json.loads(result.stdout)
            self.extract_password(item_details)
            self.extract_max_length(item_details)
        except subprocess.CalledProcessError as e:
            self.failed_tests.append({"test": "fetch_details", "message": str(e), "critical": True})

    def extract_password(self, item_details):
        for field in item_details.get('fields', []):
            if field.get('id') == 'password' or field.get('label').lower() == 'password':
                self.password = field.get('value')
                break

    def extract_max_length(self, item_details):
        for field in item_details.get('fields', []):
            if field.get('label') == MAX_LENGTH_FIELD_NAME:
                try:
                    self.max_length = int(field.get('value'))
                except ValueError:
                    self.max_length = None
                break

    def check_password_length(self, ideal_length):
        if self.password:
            password_length = len(self.password)
            if password_length < ideal_length:
                if self.max_length:
                    if password_length == self.max_length:
                        self.failed_tests.append({"test": "password_length", "message": f"Password matches the maximum allowed length ({self.max_length} characters)", "critical": False})
                    else:
                        self.failed_tests.append({"test": "password_length", "message": f"Password too short: {password_length} characters. Maximum length provided, but not used ({self.max_length} characters)", "critical": True})
                else:
                    if OWNERSHIP_TAG in self.tags:
                        self.failed_tests.append({"test": "password_length", "message": f"Password too short: {password_length} characters, but tagged as somebody else's account", "critical": False})
                    else:
                        self.failed_tests.append({"test": "password_length", "message": f"Password too short: {password_length} characters", "critical": True})
        else:
            self.failed_tests.append({"test": "password_presence", "message": "No password found", "critical": True})

    def print_results(self):
        if not self.failed_tests:
            print_green(f"All checks passed for \"{self.title}\"")
        else:
            critical_failures = any(test['critical'] for test in self.failed_tests)
            if critical_failures:
                print_red(f"Critical issues found for \"{self.title}\":")
                for test in self.failed_tests:
                    print_red(f"  - {test['test']}: {test['message']}")
            else:
                print_yellow(f"Issues found for \"{self.title}\":")
                for test in self.failed_tests:
                    print_yellow(f"  - {test['test']}: {test['message']}")

# Start timing
start_time = time.time()

# Fetch all items from the vault
try:
    result = subprocess.run(['op', 'item', 'list', '--format', 'json'], capture_output=True, text=True, check=True)
    items = json.loads(result.stdout)
except subprocess.CalledProcessError as e:
    print("Error fetching items from 1Password vault.")
    print(e)
    sys.exit(1)

total_items = 0
severe_failures = 0
slight_failures = 0
failure_types = {}
skipped_items = 0

# Loop through each item
for item in items:
    if item['category'].lower() != 'login':
        skipped_items += 1
        continue

    total_items += 1
    vault_item = VaultItem(item['id'], item['title'], item['category'], item.get('tags', []))
    vault_item.fetch_details()
    vault_item.check_password_length(IDEAL_PASSWORD_LENGTH)
    vault_item.print_results()

    if vault_item.failed_tests:
        critical_failures = any(test['critical'] for test in vault_item.failed_tests)
        if critical_failures:
            severe_failures += 1
        else:
            slight_failures += 1
        for test in vault_item.failed_tests:
            test_type = test['test']
            if test_type in failure_types:
                failure_types[test_type] += 1
            else:
                failure_types[test_type] = 1

# End timing
end_time = time.time()
elapsed_time = end_time - start_time

# Print summary
print("\nSummary:")
print(f"Total passwords checked: {total_items}")
print(f"Total severe failures: {severe_failures}")
print(f"Total slight failures: {slight_failures}")
print(f"Total items skipped: {skipped_items}")
print("Failure breakdown:")
for test_type, count in failure_types.items():
    print(f"  {test_type}: {count}")

# Print elapsed time
print(f"\nTime taken: {elapsed_time:.2f} seconds")
