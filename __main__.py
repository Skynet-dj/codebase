from utils.requirements import install_requirements

def main():
    install_requirements()
    import main as m
    m.main()

if __name__ == "__main__":
    main()
