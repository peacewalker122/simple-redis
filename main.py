from server import Server


def main():
    server = Server("127.0.0.1", 6379)
    server.run()


if __name__ == "__main__":
    main()(287)
