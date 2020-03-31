import sys
import os
import pathlib

SUFFIX_MANAGED = ['.mkv', '.avi', '.mp4', '.vob']


def help():
	print('------------------------------')
	print('check : afficher les films qui n\'ont pas leur propre dossier')
	print('apply : créer et déplace les films dans leur propre dossier ')
	print('------------------------------')


# check all movies
def check(path = None, apply: bool = False):

	if path is None:
		path = input('enter the path :')
		print('Path is : ' + path)
		if input('confirm (y/n) : ') != 'y':
			exit(0)

	dir = pathlib.Path(path)

	if dir.exists() is False:
		print('directory "'+str(path)+'" not exist.')
		exit(1)

	if dir.is_dir() is False:
		print(str(path) + '" is not a directory.')
		exit(1)

	browse(dir, apply)


# browse dir and go deeper if needed ( recursive function )
def browse(current_dir: pathlib.Path, apply: bool = False):

	# browse directory
	for f in current_dir.iterdir():

		if f.name[0] == '$':
			continue

		if f.is_dir():
			# is directory => go deeper
			browse(current_dir.joinpath(f.name), apply)
		else :
			# current file extension managed
			if f.suffix in SUFFIX_MANAGED:
				_move = False
				_parent_directory_name = f.name.replace(f.suffix, "")

				# not move
				if current_dir.name != _parent_directory_name:
					_move = True

				if _move:
					_new_directory_path = current_dir.joinpath(_parent_directory_name)
					ndir = pathlib.Path(_new_directory_path)

					# show only
					if apply is False:
						print(str(f.name + " => deplacement requis").encode('utf-8'))


					if apply:
						if ndir.exists() is False:
							# create directory
							ndir.mkdir()
							print(str("creation dossier : " + ndir.name).encode('utf-8'))

						# check if exist
						if ndir.exists() is False:
							print(str("ERREUR durant creation du dossier " + ndir.name).encode('utf-8'))
							continue

						else:
						# move file in directory
							f.rename(_new_directory_path.joinpath(f.name))
							print(str("deplacement de : " + f.name).encode('utf-8'))



# Main bitch
if __name__ == '__main__':

	if len(sys.argv) == 1 :
		help()

	for arg in sys.argv:
		if arg == 'help':
			help()
		if arg == 'check':
			try:
				check(sys.argv[2])
			except IndexError:
				check()

		if arg == 'apply':
			try:
				check(sys.argv[2], True)
			except IndexError:
				check(None, True)



	exit(0)