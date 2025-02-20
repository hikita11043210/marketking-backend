import os,json,datetime


def generate_log_file(data, filename, time=False):
    log_dir = "logs/"
    os.makedirs(log_dir, exist_ok=True)
    if time:
        filename = f"{log_dir}{filename}_{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}.json"
    else:
        filename = f"{log_dir}{filename}.json"
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
