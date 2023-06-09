from django.shortcuts import render
from django.http import HttpResponse

from ide.settings import BASE_DIR

import subprocess
import os


# Create your views here.
def home(request):
    if request.method == "POST":
        code = request.POST["writecode"]
        customInput = "\n".join(request.POST["customInput"].split())
        with open("static/userCodes/input.txt", "w") as file:
            file.write(customInput)
        # print(code)
        output = ""
        options = "python cpp javaCode".split()
        option = ""
        for i in options:
            a = request.POST.get(i)
            if a != None:
                option = a
                break
        print(option)

        if option == "python":
            print("python selected")
            f = open("static/userCodes/code.py", "w")
            f.write(code)
            f.close()

            with open("static/userCodes/input.txt", "r") as file:
                input_data = file.read().strip()

            p = subprocess.Popen(
                ["python3", "static/userCodes/code.py"],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )

            out, error = p.communicate(input=input_data.encode())

            if p.returncode != 0:
                output = error.decode()
            else:
                output = out.decode()

            print(output)

            print(output)
        elif option == "cpp":
            print("c++ selected")
            f = open("static/userCodes/code.cpp", "w")
            f.write(code)
            f.close()
            e = subprocess.run(
                ["g++", "static/userCodes/code.cpp"], stderr=subprocess.PIPE
            )

            if e.returncode != 0:
                output = e.stderr.decode()
            else:
                subprocess.run([f"mv {BASE_DIR}/a.out static/userCodes/"], shell=True)

                # Read input from file
                with open("static/userCodes/input.txt", "r") as file:
                    input_data = file.read().strip()

                p = subprocess.Popen(
                    ["./static/userCodes/a.out"],
                    stdin=subprocess.PIPE,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                )

                out, error = p.communicate(input=input_data.encode())

                if p.returncode != 0:
                    output = error.decode()
                else:
                    output = out.decode()

            print(output)

        elif option == "javaCode":
            f = open("static/userCodes/code.java", "w")
            f.write(code)
            f.close()
            with open("static/userCodes/input.txt", "r") as file:
                customInput = file.read().strip()

            # Compile Java code
            e = subprocess.run(
                ["javac", "static/userCodes/code.java"], stderr=subprocess.PIPE
            )

            if e.returncode != 0:
                output = e.stderr.decode()
            else:
                path = os.getcwd()
                os.chdir("static/userCodes")

                # Execute Java code with input from input.txt
                output = subprocess.run(
                    ["java", "Solution"],
                    input=customInput,
                    text=True,
                    capture_output=True,
                ).stdout

                os.chdir(path)

        print(output)
        clean()
        return render(request, "home.html", context={"output": output})

    return render(request, "home.html")


def clean():
    for file in os.listdir("static/userCodes"):
        print(file)
        os.remove(f"static/userCodes/{file}")
