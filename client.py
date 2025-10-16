import requests

response = requests.post(
    "http://127.0.0.1:8081/desk/",
    json={"header": "header13", "description": "nnpqwndq213231sd", "owner": "Y"},
)
print(response.status_code)
print(response.text)

# response = requests.get("http://127.0.0.1:8081/desk/8",
#
#                          )
# print(response.status_code)
# print(response.text)

# response = requests.patch("http://127.0.0.1:8081/desk/1",
#                           json={"header": "header2"}
#
#                          )
# print(response.status_code)
# print(response.text)

# response = requests.delete("http://127.0.0.1:8081/desk/2",
#
#                          )
# print(response.status_code)
# print(response.text)
