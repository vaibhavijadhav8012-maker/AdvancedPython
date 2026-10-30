import re

email = input("Enter your email address: ")

pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

if re.fullmatch(pattern, email):
    print("Valid Email Address")
else:
    print("Invalid Email Address")
    