import socket


class URL:
    def __init__(self,url):
        self.scheme, url = url.split("://", 1)
        assert self.scheme == "http"
        
        if "/" not in url:
            url += "/"
        self.host, url = url.split("/",1)
        self.path = "/" + url
        
    def request(self):
        s = socket.socket(
            family = socket.AF_INET,
            type = socket.SOCK_STREAM,
            proto = socket.IPPROTO_TCP,
        )
        s.connect((self.host,80))
        
        request = "GET {} HTTP/1.0\r\n".format(self.path)
        request += "Host: {}\r\n".format(self.host)
        request += "\r\n"
        
        s.send(request.enconde("utf8"))
        
        response = s.makefile("r", enconding="utf8", newline = "\r\n")
        
        statusline = response.readline()
        version, status, explanation = statusline.split(" ",2)
        
        
        # Nota: Aca no estamos checkeando que la respuesta haya sido en el mismo HTTP que la pedi
        # Algunos servidores pueden llegar a devolver 1.1 envez de 1.0 por ejemplo
        # Por suerte los protocolos en un caso asi son lo suficientemnete similares como para uqe no genere problema
        
        response_headers = {}
        while True:
            line = response.readline()
            if line  == "\r\n": break
            header, value = line.split(":",1)
            response_headers[header.casefold()] = value.strip()
            
            
            #Aca checkeamos que la data no se nos devuelva de formas "inusuales"
            assert "transfer_enconding" not in response_headers
            assert "content_encoding" not in response_headers
            
            content = response.read()
            s.close
            
            return content
    
   
    def show(body):
        in_tag = False
        
    #Me quede en 1.6        