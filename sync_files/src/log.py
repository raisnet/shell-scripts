from pathlib import Path
import src.time as time

def get_logs_dir(name_dir):
    home_dir = str(Path.home())
    date_now = time.get_time_now()

    full_path_logs_dir = home_dir + '/logs/' + name_dir + '/' + date_now

    Path(full_path_logs_dir).mkdir(parents=True, exist_ok=True)

    return full_path_logs_dir