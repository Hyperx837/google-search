import sys

if __name__ == "__main__":
    major = sys.version_info[0]
    minor = sys.version_info[1]

    pyversion = (
        str(sys.version_info[0])
        + "."
        + str(sys.version_info[1])
        + "."
        + str(sys.version_info[2])
    )

    if sys.version_info >= (3, 9):
        print("Vdex is only tested on Python 3.9+\nYou are using Python {pyversion}")
        confirm = input(
            "This can cause unexpected errors. Do you wanna continue? [Y/n] "
        )
        if confirm == "n":
            sys.exit(1)

    from vdex.vdex import main

    while True:
        main()
