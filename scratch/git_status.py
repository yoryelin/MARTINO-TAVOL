import subprocess
print(subprocess.check_output(['git', 'status'], text=True))
