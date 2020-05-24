from page_load.cli import parser
from page_load.page_load import page_loader


def main():
    arguments = parser.parse_args()
    page_loader(
        arguments.target_url,
        destination=arguments.destination,
    )


if __name__ == "__main__":
    main()
