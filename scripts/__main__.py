from ..utils.requirements import install_requirements

def main(): 
    try:
        import scripts.cli as cli
        cli.main()
    except ModuleNotFoundError:
        pass

if __name__ == "__main__":
    install_requirements()
    main()
