from utils.requirements import install_requirements

def main():
    install_requirements()
    import main
    main.main()

if __name__ == "__main__":
    main()
