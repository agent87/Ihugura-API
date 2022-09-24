import requests



def send_sms(number, sms):
    token='eyJhbGciOiJub25lIn0.eyJpZCI6Mjg0LCJyZXZva2VkX3Rva2VuX2NvdW50IjowfQ.'
    headers = {'Authorization': 'Bearer ' + token}
    data = {'to' : number, 'text' : sms, 'sender' : 'Ihugura Chatbot'}

    url = 'https://api.pindo.io/v1/sms/'
    response = requests.post(url, json=data, headers=headers)
