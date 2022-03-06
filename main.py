from time import sleep

dir_path = "/sys/class/power_supply/BAT1"


def get_parameter(parameter_name: str) -> str:
    with open(dir_path + "/" + parameter_name, "r") as capacity_file:
        parameter = capacity_file.read()
    return parameter


def run_state_notifier() -> None:
    while True:
        status = get_parameter("status").strip()
        print(status)

        if status.startswith("Discharging"):
            print(get_parameter("capacity").strip())

        sleep(30)


if __name__ == '__main__':
    run_state_notifier()
