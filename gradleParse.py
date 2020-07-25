import os

rootdir = 'C:\source\Python\Open Source Learning Set\Java\spring-boot-master'
fileList = []

for subdir,dirs,files in os.walk(rootdir):
    for file in files:
        if "build.gradle" in file:
            fileList.append(os.path.join(subdir,file))

for files in fileList:
    dependencyList = []
    inDependency = False
    bracketCount = 0

    f = open(files,"r")
    for lines in f.readlines():
        if inDependency:
            if "{" in lines:
                bracketCount += 1
            if "}" in lines:
                bracketCount -= 1

            if bracketCount == 0:
                inDependency = False
            else:
                dependencyList.append(lines.strip())
        if "dependencies {" in lines:
            inDependency = True
            bracketCount += 1

    print(files)
    for lines in dependencyList:
        print(lines)