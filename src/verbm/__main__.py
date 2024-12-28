from verbm.run import run


def main():
    try:
        run()
    except Exception as ex:
        # error only, without the stacktrace
        print(ex)
        exit(1)


if __name__ == "__main__":
    main()
