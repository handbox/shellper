import sys

import argparse
import yaml

import shellper.base as base
import shellper.validation as validation


def add_links(google, config):
    for event in config:
        event["description"] = []
        event["description"].append(google.search_query(event["summary"]))


def parsing_args():
    parser = argparse.ArgumentParser(description="Parser")
    parser.add_argument('argument', help="Path to template file",
                        nargs='?')
    args = parser.parse_args()
    return args.argument


def open_file(argument):
    with open(argument, 'r') as yaml_file:
        return yaml.load(yaml_file)


def main():
    argument = parsing_args()
    config = open_file(argument)
    validation.validate(config)
    del sys.argv[-1]
    google = base.Base()

    google.get_event_list()
    add_links(google, config)
    for event in config:
        google.create_event(event)

if __name__ == "__main__":
    main()
