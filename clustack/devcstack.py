from builder import Builder
from envmanager import EnvManager

def allsteps():
    testBuilder = Builder('zlib', 'http://zlib.net/zlib-1.2.8.tar.gz')
    testBuilder._version = '1.2.8'
    # testBuilder = Builder('libpng', 'https://downloads.sf.net/project/libpng/libpng16/1.6.15/libpng-1.6.15.tar.xz')
    # testBuilder._version = '1.6.15'

    # testBuilder = Builder('lesstiff', 'https://downloads.sourceforge.net/project/lesstif/lesstif/0.95.2/lesstif-0.95.2.tar.bz2')
    # testBuilder._version = '0.95.2'

    testBuilder.download()
    testBuilder.unpack()
    testBuilder.configure()
    testBuilder.build()
    testBuilder.install()

def main():
    # testBuilder = Builder('zlib', 'http://zlib.net/zlib-1.2.8.tar.gz', False)
    # testBuilder._version = "1.2.8"

    # print testBuilder.build_dir

    # myenv = EnvManager()

    # print myenv.PATH

    allsteps()

if __name__ == "__main__":
    main()
