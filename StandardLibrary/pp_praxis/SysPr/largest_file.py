"""Find the largest Python source file in a single directory.Search Windows Python source lib, unless dir command-line arg."""# true version throw !!! glob.glob !!!import osdef get_dir_files(dirpath):  files = []  for file in os.listdir(dirpath):    if not os.path.isdir(os.path.join(dirpath,file)):      files.append(file)      return files    def find_largest_directory_py_file(dirpath):  py_files = [file for file in get_dir_files(dirpath)                     if file[-2:] == "py"]  result = max(py_files,key=lambda file: os.path.getsize(os.path.join(dirpath,file)))   return result"""  if __name__ == "__main__":  print find_largest_directory_py_file(r"C:\Program Files\Python2.7.2\Lib")"""        """Find the largest Python source file in an entire directory tree.Search the Python source lib, use pprint to display results nicely."""    # true version with !!! str.endwith(".py") !!!    def get_py_files(filenames):  return [file for file in filenames                 if file[-2:] == "py"]  def find_largest_directory_tree_py_file(main_dirpath):  largest_file_name = ""  largest_file_size = 0  for dirpath,dirnames,filenames in os.walk(main_dirpath):      py_files = get_py_files(filenames)    if py_files != []:      r = max(py_files,key=lambda file: os.path.getsize(os.path.join(dirpath,file)))      r_name = os.path.join(dirpath,r)      r_size = os.path.getsize(r_name)      if r_size > largest_file_size:        largest_file_name = r_name        largest_file_size = r_size  return largest_file_name,largest_file_size  """  if __name__ == "__main__":  print find_largest_directory_tree_py_file(r"C:\Program Files\Python2.7.2") """"""Find the largest Python source file on the module import search path.Skip already-visited directories, normalize path and case so they willmatch properly, and include line counts in pprinted result. It's notenough to use os.environ['PYTHONPATH']: this is a subset of sys.path."""import sysdef exclude_nested_packages(dirs):    init = "__init__.py"  exc_dir_inds = []  for i,d1 in enumerate(dirs):    for d2 in dirs[i+1:]:      if len(d1) >= len(d2) and d1[:len(d2)] == d2:        d = d1        while len(d) != len(d2):          os.listdir(d)          if init not in os.listdir(d):             break;          d = os.path.split(d)[0]        else:           exc_dir_inds.append(i)          break  return [d for i,d in enumerate(dirs) if i not in exc_dir_inds] def get_file_line_quantity(filepath):  return sum(1 for line in open(filepath))  class File:  def __init__(self,path,size):    self.path = path    self.size = size  def __cmp__(self,file):    return self.size - file.size        def get_largest_visible_py_file():  init = "__init__.py"    res = File("",-1)  dirs = exclude_nested_packages([p for p in sys.path if os.path.isdir(p)])  for d in dirs:    source = True    for (dirpath,dirnames,filenames) in os.walk(d):      if not source and (init not in filenames):        dirnames[:] = []        continue      else:        source = False        py_names = get_py_files(filenames)        for py_n in py_names:          full_py_n = os.path.join(dirpath,py_n)          file = File(full_py_n,os.path.getsize(full_py_n))          if res < file:            res = file   return res.path,res.size,get_file_line_quantity(res.path)"""  if __name__ == "__main__":  print get_largest_visible_py_file()  """def count_lines(filepath):  file = open(filepath)  n = sum(1 for line in open(filepath))  file.close()  return n  def get_size(filepath):  return os.path.getsize(filepath)class File:    def __init__(self,path):    self.path = path    def __cmp__(self,file):    return self.algo()-file.algo()      def empty(self):    return self.path == ""  class FileLines(File):    def algo(self):    return count_lines(self.path)    def __init__(self,path):    File.__init__(self,path)  class FileSize(File):    def algo(self):    return get_size(self.path)    def __init__(self,path):    File.__init__(self,path)  def get_max_visible_file(File):    init = "__init__.py"    res = File("")  dirs = exclude_nested_packages([p for p in sys.path if os.path.isdir(p)])    for d in dirs:    source = True    for (dirpath,dirnames,filenames) in os.walk(d):      if not source and (init not in filenames):        dirnames[:] = []        continue      else:        source = False        py_names = get_py_files(filenames)        for py_n in py_names:           file = File(os.path.join(dirpath,py_n))          if res.empty() or (res < file):            res = file                          return res.path    """  if __name__ == "__main__":  path = get_max_visible_file(FileSize)  print path,count_lines(path)"""            def get_max_file_on_drive(drive,File):  res = File("")  for (dirpath,dirnames,filenames) in os.walk(drive):    py_names = get_py_files(filenames)    for py_n in py_names:       file = File(os.path.join(dirpath,py_n))      if res.empty() or (res < file):        res = file  return res.path  if __name__ == "__main__":  path = get_max_file_on_drive("C:/",FileSize)    print path,FileSize(path).algo()        