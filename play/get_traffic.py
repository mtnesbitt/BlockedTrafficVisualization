import requests

def main():
    while True:
        r = requests.get('http://10.230.1.59:5000')
        print(r.text)

if __name__ == "__main__":
    main()