import socket
try:
    print(f"IP of martinoagromaquinarias.com.ar: {socket.gethostbyname('martinoagromaquinarias.com.ar')}")
except Exception as e:
    print(f"Error lookup martinoagromaquinarias.com.ar: {e}")

try:
    print(f"IP of www.martinoagromaquinarias.com.ar: {socket.gethostbyname('www.martinoagromaquinarias.com.ar')}")
except Exception as e:
    print(f"Error lookup www.martinoagromaquinarias.com.ar: {e}")
