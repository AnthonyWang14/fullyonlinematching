import csv

def change_file_format(input_file, output_file):
    with open(input_file, 'r') as infile, open(output_file, 'w', newline='') as outfile:
        reader = csv.reader(infile, delimiter=' ')
        writer = csv.writer(outfile)
        for row in reader:
            if row:
                writer.writerow(row)

if __name__ == '__main__':
    input_file = 'output.txt'
    output_file = 'output.csv'
    change_file_format(input_file, output_file)