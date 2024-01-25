import csv

def analyze_results(analysed_file):
    with open(analysed_file) as file_input:
        file = file_input.read().splitlines()

    smoke_status_code = []
    temp_status_code = []
    elapsed_time = []

    for i in range(1, len(file)):
        data = file[i].split(',')
        smoke_status_code.append(data[1])
        temp_status_code.append(data[2])
        if data[3]:
            elapsed_time.append(float(data[3]))

    smoke_ok = smoke_status_code.count('201')
    temp_ok = temp_status_code.count('201')
    avg_time = round(max(elapsed_time) / (len(elapsed_time)), 7)
    smoke_eff = round(smoke_ok / len(smoke_status_code) * 100, 3)
    temp_eff = round(temp_ok / len(temp_status_code) * 100, 3)

    return len(file) - 1, smoke_eff, temp_eff, avg_time

def write_results_to_csv(test_position):
    shieldbox_nums = [10, 15, 25, 50, 100, 150, 250, 500, 1000]

    with open(f"results_{test_position}.csv", 'w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(['Number of Shieldboxes', 'Smoke Value Efficiency', 'Temp Value Efficiency', 'Average Response Time'])

        for shieldbox_num in shieldbox_nums:
            file_name = f"test_results_{shieldbox_num}_{test_position}.csv"
            results = analyze_results(file_name)
            csv_writer.writerow(results)

# List of test positions: 1, 2, 3
for test_position in [1, 2, 3]:
    write_results_to_csv(test_position)
