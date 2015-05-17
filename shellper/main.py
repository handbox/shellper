import sys

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
    del sys.argv[-1]
    google = base.Base()

    google.get_event_list()
    for event in config:
        event["description"] = []
        event["description"].append(google.search_query(event["summary"]))
    for event in config:
        id = google.create_event(event)
        google.delete_event(id)

if __name__ == "__main__":
    main()
