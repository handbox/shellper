import argparse
import yaml

import shellper.base as base
import shellper.validation as validation


def main():
    # parse args
    parser = argparse.ArgumentParser(description="Parser")
    parser.add_argument('argument', help="Path to template file",
                        nargs='?')
    args = parser.parse_args()
    argument = args.argument
    with open(argument, 'r') as yaml_file:
        config = yaml.load(yaml_file)

    validation.validate(config)

    google = base.Base()
    links = []
    for event in config:
        links.append(google.search_query(event["summary"]))

if __name__ == "__main__":
    main()
