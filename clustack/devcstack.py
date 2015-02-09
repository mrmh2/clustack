from shelf import Shelf

def main():
    s = Shelf()

    all_packages = s.installed_packages

    print all_packages['samtools'].bin_dir


if __name__ == "__main__":
    main()
