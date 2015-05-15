import argparse
import shellper.validation as validation
import yaml


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

if __name__ == "__main__":
    main()
