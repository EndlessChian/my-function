from distutils.core import setup, Extension
import os
module = Extension('_graphics', sources=['graphics.c'])

# os.sys.path.append('D:\\python\\Lib\\site-packages\\numpy')
# setup(distclass=MyDistribution)
setup(
    name = '_graphics',
    version = '1.0',
    description = 'This is a python package of a graphics proccession for numpy.',
    ext_modules = [module],
    author = 'JinChen<miracle@stu2022.jnu.edu.cn>',
)
# cl /LD /I/python/include graphics.c ../libs/python311.lib