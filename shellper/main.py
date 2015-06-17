import sys

import argparse
import yaml

import shellper.base as base
import shellper.validation as validation


# Add results to event description
def add_links(google, config):
    for event in config:
        event["description"] = []
        if google.search_query(event["summary"]):
            event["description"].append(google.search_query(event["summary"]))
        else:
            event["description"].append(["Results_not_found"])


# Parsing of arguments from tox
def parsing_args():
    parser = argparse.ArgumentParser(description="Parser")
    parser.add_argument('argument', help="Path to template file",
                        nargs='?')
    args = parser.parse_args()
    return args.argument


# Open yaml file and conver to json
def open_file(argument):
    with open(argument, 'r') as yaml_file:
        return yaml.load(yaml_file)


def main():
    argument = parsing_args()
    config = open_file(argument)
    validation.validate(config)
    del sys.argv[-1]
    google = base.Base()

    event_list = google.get_event_list()
    if event_list:
        for event in event_list:
            print event
    else:
        print 'No upcomings events found'
    add_links(google, config)
    for event in config:
        google.create_event(event)

if __name__ == "__main__":
    main()
