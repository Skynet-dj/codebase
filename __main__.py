from utils.requirements import install_requirements


def boss():
    install_requirements()
    import cli
    cli.main()

if __name__ == "__main__":
    boss()
