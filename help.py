import json
from collections import defaultdict, OrderedDict

# Đọc dữ liệu từ file JSON
with open('nhatot.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Tạo một defaultdict để nhóm dữ liệu
grouped_data = defaultdict(list)

# Nhóm dữ liệu
for item in data:
    region = item.get('region')
    if region is not None:
        grouped_data[region].append(item)

# Sắp xếp dữ liệu theo khóa "region"
sorted_grouped_data = OrderedDict(sorted(grouped_data.items()))

# Chuyển OrderedDict thành dict thông thường
sorted_grouped_data = dict(sorted_grouped_data)

# Xuất dữ liệu đã nhóm và đã sắp xếp vào một file JSON khác nếu cần
with open('sorted_grouped_data.json', 'w', encoding='utf-8') as f:
    json.dump(sorted_grouped_data, f, indent=4, ensure_ascii=False)

# Hoặc in ra màn hình để kiểm tra

