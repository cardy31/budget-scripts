# This script converts the default Tangerine CSV format into the format I want for my budget
#
# Example: python3 expense_converter.py /Users/cardy/Downloads/expenses.csv 9 Rob

import csv
import sys
import time
from pathlib import Path


class ExpenseFixer:
    def __init__(self):
        if len(sys.argv) != 4:
            print("Expected args: <file_to_open> <valid_month> <name>")
            exit(1)

        self.file_to_open = sys.argv[1]
        self.valid_month = int(sys.argv[2])
        self.person = sys.argv[3]

        if self.valid_month < 1 or self.valid_month > 12:
            print("The second argument must be a number representing the valid month, 1-12")
            exit(1)

    def run(self):
        try:
            with open(self.file_to_open) as csvfile:
                reader = csv.reader(csvfile)

                with open(f'{Path.home()}/Downloads/expenses_formatted.csv', 'w') as formattedCsvFile:
                    writer = csv.writer(formattedCsvFile)
                    all_rows = []
                    first_row = ""
                    for i, row in enumerate(reader):
                        # First row is a header, so handle it separately
                        if i == 0:
                            first_row = self.fix_first_row(row)
                            continue

                        # Skip entries that aren't expenses
                        if row[1] == "CREDIT":
                            continue

                        row = self.fix_data_row(row)
                        if row is None:
                            continue

                        all_rows.append(row)

                    all_rows = self.format_all_rows(all_rows, first_row)
                    writer.writerows(all_rows)
        except OSError:
            print("The first argument must be a valid path to the CSV file to convert. Full path required (no ~/...)")

    @staticmethod
    def fix_first_row(row):
        row.pop(1)
        row.insert(2, "Person")
        row[3] = "Category"
        return row

    def fix_data_row(self, row):
        # Convert string date to python struct
        row[0] = time.strptime(row[0], "%m/%d/%Y")

        # If the month is wrong then drop the row
        if getattr(row[0], "tm_mon") != self.valid_month:
            return None

        # Delete the second column
        row.pop(1)

        # Add a new column with the name of the person
        row.insert(2, self.person)

        # Clear the fourth column
        row[3] = ""

        # Change negative number to positive in fifth column
        row[4] = f'${str(abs(float(row[4])))}'

        return row

    @staticmethod
    def format_all_rows(all_rows, first_row):
        # Sort rows by date
        all_rows.sort(key=lambda x: x[0])

        # Convert date back into a human-readable string
        for row in all_rows:
            row[0] = time.strftime("%b %-d", row[0])

        # Add header row back in
        all_rows.insert(0, first_row)

        return all_rows


if __name__ == '__main__':
    ExpenseFixer().run()


