# This script takes two CSV files and dedupes their rows. Helpful for importing expenses.
#
# Example: python3 dedupe.py /Users/cardy/Downloads/expenses.csv /Users/cardy/Downloads/more_expenses.csv


import csv
import sys
import time
from pathlib import Path


class DeDuper:
    def __init__(self):
        if len(sys.argv) != 3:
            print("Expected args: <file_one> <file_two>")
            exit(1)

        self.file_one = sys.argv[1]
        self.file_two = sys.argv[2]

    def run(self):
        files = []
        for file in [self.file_one, self.file_two]:
            try:
                files.append(open(file))
            except OSError:
                print("The first file is not a valid filepath")
                exit(1)

        readers = []
        for file in files:
            readers.append(csv.reader(file))

        all_rows = []
        first_row = ""

        for reader in readers:
            for row in reader:
                if row[0] == "Transaction date":
                    first_row = row
                    continue
                all_rows.append(row)

        all_rows = set(tuple(i) for i in all_rows)
        all_rows = list(all_rows)

        for idx, row in enumerate(all_rows):
            row = list(row)
            row[0] = time.strptime(row[0], "%b %d")
            all_rows[idx] = row
        all_rows.sort(key=lambda x: x[0])

        for row in all_rows:
            row[0] = time.strftime("%b %-d", row[0])

        all_rows.insert(0, first_row)

        fileout = open(f'{Path.home()}/Downloads/deduped.csv', 'w')
        writer = csv.writer(fileout)
        writer.writerows(all_rows)


if __name__ == '__main__':
    DeDuper().run()
