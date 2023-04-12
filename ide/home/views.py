from django.shortcuts import render
from django.http import HttpResponse

from ide.settings import BASE_DIR

import subprocess

# Create your views here.
def home(request):
    if (request.method=='POST'):
        code = request.POST['writecode']
        # print(code)

        output = ""

        options = 'python cpp java'.split()
        option = ""
        for i in options:
            a = request.POST.get(i)
            if (a!=None):
                option = a
                break
        print(option)

        if (option=='python'):   

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
            f = open('static/userCodes/code.cpp','w')
            f.write(code)
            f.close()
            e = subprocess.run('g++ static/userCodes/code.cpp'.split())
            if (e.returncode!=0):
                output = e.stderr
            else:
                subprocess.run(f'mv {BASE_DIR}/a.out static/userCodes/'.split())
                output = subprocess.run(['./static/userCodes/a.out'],stdout=subprocess.PIPE).stdout.decode()

        return render(request,'home.html', context={'output':output})

    return render(request,"home.html")