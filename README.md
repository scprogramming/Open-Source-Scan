The Scprogramming Open Source Detector Project is a project to allow developers to scan their applications to find what open source and external references are being used in their code. The goal is to allow developers to have an easy way to determine risk, generate bill of materials, and know what files are impacted by changes to external dependencies

## Install
This project uses Python, with a web front end built in Flask. 

To install the dependencies, you can run the following commands:
```
pip install Flask
pip install requests
```

Once this is completed, you can run the web server through /app/__init__.py using the command:
```
python3 __init__.py
```

Once this is done, you can access the web interface for the project through 127.0.0.1:5000

###Features and Usage
Currently, the following features are implemented in Open Source Detector:
	1. The ability to scan multiple projects multiple times for dependencies
	2. Generate a list of dependencies, where they are located, the versions if available, and potential CVEs that exist in the open source.
	
The application currently supports the following languages and build enviroments:
	-Java
		-Gradle
		
For full documentation of the code and functionality, visit www.scprogramming.com