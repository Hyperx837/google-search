import sys

if __name__ == "__main__":
    if sys.version_info < (3, 9):
        print("Vdex is only tested on Python 3.9+\nYou are using Python {}.{}.{}".format(*sys.version_info))
        confirm = input(
            "This can cause unexpected errors. Do you wanna continue? [Y/n] "
        )
        if confirm == "n":
            sys.exit(1)

    from vdex.vdex import main

    main()
