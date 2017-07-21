import requests

def main():
        r = requests.get('http://10.230.1.59:5000/timestamp?t=2017/07/21 12:20:00')
        print(r.text)

if __name__ == "__main__":
    main()