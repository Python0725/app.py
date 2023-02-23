import json


def read_file(filename):
    with open(filename, 'r') as f:
        lines = f.readlines()
    return lines


def parse_data(lines):
    data = []
    for line in lines:
        if line.startswith((':', '#')):
            continue
        else:
            year = int(line[0:4])
            month = int(line[5:7])
            day = line[8:10].strip().zfill(2)
            hour = int(line[11:13])
            minute = int(line[13:15])
            speed = float(line[41:49])
            try:
                status = int(line[50])
            except ValueError:
                status = 0  # 或其他你想要设置的默认值
            if speed >= 0:
                data.append({'year': year, 'month': month, 'day': day, 'hour': hour, 'minute': minute, 'speed': speed,
                             'status': status})
    return data


def compute_daily_average(data):
    daily_averages = {}
    for entry in data:
        year = entry['year']
        month = entry['month']
        day = entry['day']
        speed = entry['speed']
        if (year, month, day) not in daily_averages:
            daily_averages[(year, month, day)] = {'count': 0, 'sum': 0}
        daily_averages[(year, month, day)]['count'] += 1
        daily_averages[(year, month, day)]['sum'] += speed
    for key in daily_averages:
        daily_averages[key]['average'] = daily_averages[key]['sum'] / daily_averages[key]['count']
    return daily_averages


def compute_level(daily_averages):
    levels = {}
    for key in daily_averages:
        average = daily_averages[key]['average']
        if average >= 500:
            levels[key] = 1
        elif average >= 300:
            levels[key] = 2
        elif average >= 100:
            levels[key] = 3
        else:
            levels[key] = 4
    return levels


def output_to_json(data, levels, output_filename):
    output_data = []
    for key in levels:
        year, month, day = key
        level = levels[key]
        for entry in data:
            if entry['year'] == year and entry['month'] == month and entry['day'] == day:
                output_data.append(
                    {'year': year, 'month': month, 'day': day, 'hour': entry['hour'], 'minute': entry['minute'],
                     'speed': entry['speed'], 'status': entry['status'], 'level': level})
                break
    with open(output_filename, 'w') as f:
        json.dump(output_data, f)


if __name__ == '__main__':
    lines = read_file('D:\ZHUOMIAN\HY\FY4A\\202212_ace_swepam_1h.txt')
    data = parse_data(lines)
    daily_averages = compute_daily_average(data)
    levels = compute_level(daily_averages)
    output_to_json(data, levels, 'output.json')
