import pycurl
import json

URL = "http://localhost:5600"

def handle_response(data):
    """Process response line by line."""
    for line in data.decode("utf-8").splitlines():
        if line.strip():  # Ignore empty lines
            json_obj = json.loads(line)
            print(json_obj)  # Process the JSON object as needed

def curl_file(file_path):
    # Initialize pycurl
    c = pycurl.Curl()
    c.setopt(c.URL, URL)
    c.setopt(c.POST, 1)

    with open(file_path, "rb") as f:
        c.setopt(c.POSTFIELDS, f.read())
    c.setopt(c.WRITEFUNCTION, handle_response)

    # Perform the request
    c.perform()
    c.close()


curl_file("8108133011_1543079686.dem")