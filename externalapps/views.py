from django.http import HttpResponse
from Crypto.PublicKey import RSA
import base64

def generate_passcode(request):
    s = RSA.Random.get_random_bytes(128)
    s = base64.b64encode(s).decode('ascii')
    s = s.replace('=', '').replace('+', '-').replace('/', '_')
    return HttpResponse(s)
