import os
import csv


class ExportJob:

    def __init__(self, options):
        self.options = options

    def resolve_output(self, name):
        folder = self.options["exports"]
        output_file = os.path.join(folder, name)
        return output_file

    def write_rows(self, name, rows):
        target = self.resolve_output(name)

        with open(target, "w", newline="", encoding="utf-8") as sink:
            writer = csv.writer(sink)
            writer.writerows(rows)


def main():
    config = {"exports": os.path.join(os.getcwd(), "exports")}
    job = ExportJob(config)

    filename = input("export file: ").strip()
    rows = [["id", "value"], ["1", "demo"], ["2", "sample"]]

    job.write_rows(filename, rows)


if __name__ == "__main__":
    main()