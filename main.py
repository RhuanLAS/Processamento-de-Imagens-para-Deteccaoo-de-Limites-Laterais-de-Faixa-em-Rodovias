import os

from src.manage_display import ManageDisplay


def main() -> None:
    path = f'{os.getcwd()}/data'

    manage_display = ManageDisplay(
        data_path = path
    )

    manage_display.workflow()

if __name__ == '__main__':
    main()