dir_path = "/sys/class/power_supply/BAT1"


def get_parameter(parameter: str):
    with open(dir_path + "/" + parameter, "r") as capacity_file:
        capacity = capacity_file.read()
    return capacity


if __name__ == '__main__':
    print(get_parameter("status"))
    print(get_parameter("capacity"))
