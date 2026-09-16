import csv
import json


# Read CSV file
def read_csv(input_path):
    with open(input_path, "r", newline="") as f:
        reader = csv.DictReader(f)
        return list(reader)


# Write data to JSON file
def write_json(output_path, data):
    with open(output_path, "w") as f:
        json.dump(data, f, indent=4)


# Convert CSV to JSON
def convert_csv_to_json(input_path, output_path):
    data = read_csv(input_path)
    write_json(output_path, data)
    return data


# Main program
if __name__ == "__main__":

    input_path = "students.csv"
    output_path = "students.json"

    # Create sample CSV file
    sample_csv = (
        "id,name,department,marks\n"
        "1,Aditi Sharma,Computer Science,88\n"
        "2,Rahul Verma,Mechanical,76\n"
        "3,Sneha Iyer,Electronics,92\n"
    )

    with open(input_path, "w", newline="") as f:
        f.write(sample_csv)

    print(f"Created sample CSV file: {input_path}\n")

    # Display CSV contents
    print(f"Contents of '{input_path}':")

    with open(input_path, "r") as f:
        print(f.read())

    # Convert CSV to JSON
    data = convert_csv_to_json(input_path, output_path)

    print(f"Converted {len(data)} row(s) from CSV to JSON.")
    print(f"JSON written to: {output_path}\n")

    # Display JSON contents
    print(f"Contents of '{output_path}':")

    with open(output_path, "r") as f:
        print(f.read())