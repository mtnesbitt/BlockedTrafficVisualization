import requests
import ast

def main():
        r = requests.get('http://10.230.1.59:5000/timestamp?t=2017/07/21 12:20:00')
        list = ast.literal_eval(str(r.text))
        for a in list:
            print(a)

if __name__ == "__main__":
    main()