import subprocess

files = [
         './edge-sim - Uniform/main.py',
         './edge-sim - SORL-Tabular/main.py',
         './edge-sim - SORL-Deep/main.py',
         './edge-sim - MORL-Tabular/main.py',
         './edge-sim - MORL-Deep/main.py'
    ]
for file in files:
    process = subprocess.Popen(['python',file],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    stdout,stderr = process.communicate()
    if stderr:
        print(stderr.decode())
        break
    print(stdout.decode())
