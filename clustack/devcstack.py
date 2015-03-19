from shelf import Shelf
from stack import Stack

def main():
	s = Stack()

	s.add_by_name('python', add_dependencies=True)

	print s.included_components

	s.shell()

	#s.add_by_name('python')

	#s.shell()

	#print s.installed_packages
    #stuff('bowtie2')
    #print load_templated_yaml_rep('samtools')



if __name__ == "__main__":
    main()
