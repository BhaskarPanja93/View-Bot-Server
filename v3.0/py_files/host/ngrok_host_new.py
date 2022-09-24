from requests import get

xml_data = eval(get("http://127.0.0.1:4010/api/tunnels").text.replace("false", "False").replace("true","True"))
tunnels = xml_data["tunnels"]
for index in range(len(tunnels)):
    del tunnels[index]["metrics"]
    del tunnels[index]["config"]
    del tunnels[index]["uri"]
    del tunnels[index]["proto"]
    print(tunnels[index]['name'], tunnels[index]['public_url'])

adfly_ngrok_config="""
region: in
authtoken: 2DcFLz4kDWgTfkoacSGOSPwzrCL_7iVhooTMGr8QqfiD5A995
web_addr: 127.0.0.1:4000
inspect_db_size: -1
log_level: crit
tunnels:
    viewbot_socket:
        addr: 192.168.1.5:65499
        inspect: false
        proto: tcp
    viewbot_site:
        addr: 192.168.1.5:65500
        inspect: false
        proto: http
        schemes:
            - https
            - http
version: "2"
"""

minecraft_ngrok_config="""
region: in
authtoken: 2DcFZvIBBfSxHswi1uEilJiOCgM_W5xTFuKVMuqdB8ToSbJk
web_addr: 127.0.0.1:4001
inspect_db_size: -1
log_level: crit
tunnels:
    minecraft:
        addr: 192.168.1.5:60000
        inspect: false
        proto: tcp
version: "2"
"""
