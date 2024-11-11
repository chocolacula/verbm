from verbum.run import run


def main():
    try:
        run()
    except Exception as ex:
        # error only, without the stacktrace
        print(ex)


if __name__ == "__main__":
    main()
