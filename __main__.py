from utils.requirements import install_requirements
from cli import main as cli_main

def main():
    install_requirements()
    cli_main()

if __name__ == "__main__":
    main()
