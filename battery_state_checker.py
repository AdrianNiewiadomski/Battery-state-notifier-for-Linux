dir_path = "/sys/class/power_supply/BAT1"


def get_parameter(parameter_name: str) -> str:
    with open(dir_path + "/" + parameter_name, "r") as capacity_file:
        parameter = capacity_file.read()
    return parameter
