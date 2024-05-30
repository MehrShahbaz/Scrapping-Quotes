import sys
import os


def main():
    if len(sys.argv) < 2:
        print("Usage: python main.py <option>")
        return

    option = sys.argv[1]

    if option == "as":
        os.system("python app.py")
    elif option == "ap":
        os.system("python app_multiprocessing.py")
    elif option == "ac":
        os.system("python app_concurrent_futures.py")
    else:
        print(
            "Invalid option.Use:\n'as' for app.py\n'ap' for app_multiprocessing.py\n'ac' for app_concurrent_futures.py"
        )


if __name__ == "__main__":
    main()
