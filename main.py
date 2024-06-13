import json
import subprocess
import sys
import time

# Define the ideal password length
IDEAL_PASSWORD_LENGTH = 64
if len(sys.argv) > 1:
    try:
        IDEAL_PASSWORD_LENGTH = int(sys.argv[1])
    except ValueError:
        print("Invalid input for ideal password length. Using default value of 64.")

# Function to print in green
def print_green(text):
    print(f"\033[0;32m{text}\033[0m")

# Function to print in yellow
def print_yellow(text):
    print(f"\033[0;33m{text}\033[0m")

# Function to print in red
def print_red(text):
    print(f"\033[0;31m{text}\033[0m")

class VaultItem:
    def __init__(self, item_id, title):
        self.item_id = item_id
        self.title = title
        self.password = None
        self.failed_tests = []

    def fetch_details(self):
        try:
            result = subprocess.run(['op', 'item', 'get', self.item_id, '--format', 'json'], capture_output=True, text=True, check=True)
            item_details = json.loads(result.stdout)
            self.extract_password(item_details)
        except subprocess.CalledProcessError as e:
            self.failed_tests.append({"test": "fetch_details", "message": str(e), "critical": True})

    def extract_password(self, item_details):
        for field in item_details.get('fields', []):
            if field.get('id') == 'password' or field.get('label').lower() == 'password':
                self.password = field.get('value')
                break

    def check_password_length(self, ideal_length):
        if self.password:
            if len(self.password) < ideal_length:
                self.failed_tests.append({"test": "password_length", "message": f"Password too short: {len(self.password)} characters", "critical": True})
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

# Loop through each item
for item in items:
    total_items += 1
    vault_item = VaultItem(item['id'], item['title'])
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
print("Failure breakdown:")
for test_type, count in failure_types.items():
    print(f"  {test_type}: {count}")

# Print elapsed time
print(f"\nTime taken: {elapsed_time:.2f} seconds")
