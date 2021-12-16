import socket,ssl
import OpenSSL
import time,datetime

def get_server_certificate(host, port, sni):
    context = ssl.SSLContext()
    context.verify_mode = ssl.CERT_NONE
    context.check_hostname = False
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(1)
    with context.wrap_socket(s, server_hostname=sni) as sslSocket:
        sslSocket.connect((host, port))
        dercert = sslSocket.getpeercert(True)
        return ssl.DER_cert_to_PEM_cert(dercert)

def get_ssl_status(host:str, sni:str, remarks: str, warning:int = 7, port:int = 443) -> dict:
    ssl_status = {
        #"host": host,
        "domain": sni,
        "remarks": remarks,
        "subject": None, # *.baidu.com, baidu.com
        "start": None,  # 2021-10-09 00:00:00
        "expire": None, # 2022-10-08 23:59:59
        "issuer": None, #C=US; O=Cloudflare, Inc.; CN=Cloudflare Inc ECC CA-3
        "status": '连接错误', # 有效/即将失效/失效
        "statuscolor": "error", # success/warning/error
        "check": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), # 2021-10-29 00:24:41
        "remain": None, # 365
    }
    try:
        cert = get_server_certificate(host, port, sni)
    
        x509 = OpenSSL.crypto.load_certificate(OpenSSL.crypto.FILETYPE_PEM, cert)
        # print(x509.__dir__())

        dt_notAfter = time.strptime(x509.get_notAfter().decode("UTF-8"), '%Y%m%d%H%M%SZ')
        ssl_status["expire"] = time.strftime("%Y-%m-%d %H:%M:%S" , dt_notAfter)
        dt_notBefore = time.strptime(x509.get_notBefore().decode("UTF-8"), '%Y%m%d%H%M%SZ')
        ssl_status["start"] = time.strftime("%Y-%m-%d %H:%M:%S" , dt_notBefore)

        t_notAfter = time.mktime(dt_notAfter)
        t_now = time.time()
        time_remain = (t_notAfter - t_now) / 3600 / 24
        if time_remain > warning:
            ssl_status["status"] = "有效"
            ssl_status["statuscolor"] = "success"
        elif time_remain > 0:
            ssl_status["status"] = "即将失效"
            ssl_status["statuscolor"] = "warning"
        else:
            ssl_status["status"] = "失效"
            ssl_status["statuscolor"] = "error"
        ssl_status["remain"] =  str(int(time_remain))

        issuer = x509.get_issuer()
        issuer_info = [ i[0].decode("UTF-8")+ '=' + i[1].decode("UTF-8") for i in issuer.get_components()]
        ssl_status["issuer"] = '; '.join(issuer_info)
        for i in range(0, x509.get_extension_count()):
            ext = x509.get_extension(i)
            if b'subjectAltName' == ext.get_short_name():
                content = ext.__str__()
                domains = [ d.strip()[4:] for d in content.split(",")]
                ssl_status["subject"] = (', '.join(domains))
    except Exception as e:
        print(e)
        raise e

    return ssl_status


if __name__ == "__main__":
    import os, json
    config = os.getenv('MY_DOMAINS')
    if not config:
        with open('config.json', 'r', encoding='utf-8') as f:
            config = f.read()
            print(config)
    
    config = json.loads(config)

    ssl_status = [get_ssl_status(**conf) for conf in config]
    with open('result.json', 'w', encoding='utf-8') as f:
        f.write(json.dumps(ssl_status, ensure_ascii=False))
