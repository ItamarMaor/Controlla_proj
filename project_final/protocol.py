import re

#local ip depends on computer ip
LOCAL_IP = '192.168.1.145'
# Server address and length field size constants
SERVER_ADDRESS = (LOCAL_IP, 5457)

#regex to get the function server uses
REGEX_GET_FUNCTION = r'^\S*'

#function that uses regex to get functiom
def get_function(data):
    return re.match(REGEX_GET_FUNCTION, data)