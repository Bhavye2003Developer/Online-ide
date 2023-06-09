import os
for file in os.listdir("static/userCodes"):
    print(file)
    os.remove(f"static/userCodes/{file}")