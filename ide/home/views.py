from django.shortcuts import render
from django.http import HttpResponse

from ide.settings import BASE_DIR

import subprocess
import os

# Create your views here.
def home(request):
    if (request.method=='POST'):
        code = request.POST['writecode']
        # print(code)

        output = ""

        options = 'python cpp javaCode'.split()
        option = ""
        for i in options:
            a = request.POST.get(i)
            if (a!=None):
                option = a
                break
        print(option)

        if (option=='python'):   
            print("python selected")
            f = open('static/userCodes/code.py','w')
            f.write(code)
            f.close()

            p = subprocess.Popen('python3 static/userCodes/code.py'.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)

            out, error = p.communicate()

            if (p.returncode!=0):
                output = error.decode()
            else:
                output = subprocess.run('python3 static/userCodes/code.py'.split(),stdout=subprocess.PIPE).stdout.decode()

            print(output)
        elif (option=='cpp'):
            print("c++ selected")
            f = open('static/userCodes/code.cpp','w')
            f.write(code)
            f.close()
            e = subprocess.run('g++ static/userCodes/code.cpp'.split())
            if (e.returncode!=0):
                output = e.stderr
            else:
                subprocess.run(f'mv {BASE_DIR}/a.out static/userCodes/'.split())
                output = subprocess.run(['./static/userCodes/a.out'],stdout=subprocess.PIPE).stdout.decode()

        elif (option=='javaCode'):
            f = open('static/userCodes/code.java','w')
            f.write(code)
            f.close()
            e = subprocess.run('javac static/userCodes/code.java'.split())
            if (e.returncode!=0):
                output = e.stderr
            else:
                path = os.getcwd()
                os.chdir("static/userCodes")
                # subprocess.run(f'mv {BASE_DIR}/Solution static/userCodes/'.split())
                output = subprocess.run('java Solution'.split(),stdout=subprocess.PIPE).stdout.decode()
                print(output)
                os.chdir(path)

        return render(request,'home.html', context={'output':output})

    return render(request,"home.html")