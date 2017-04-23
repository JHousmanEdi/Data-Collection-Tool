from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need
# fine tuning.
buildOptions = dict(packages = [], excludes = [])

import sys
base = 'Win32GUI' if sys.platform=='win32' else None

executables = [
    Executable('Collection_Tool.py', base=base, targetName = 'EZCollect')
]
setup(name='EZCollect',
      version = '0.1',
      description = 'Data-Collection-Tool',
      options = dict(build_exe = buildOptions),
      executables = executables)
