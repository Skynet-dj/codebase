from .requirements import install_requirements

def main(): 
    try:
        import scripts.main as main
        main.main()
    except ModuleNotFoundError:
        pass

if __name__ == "__main__":
    install_requirements()
    main()
