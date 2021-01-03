from http.server import BaseHTTPRequestHandler, HTTPServer, SimpleHTTPRequestHandler
import logging
import os
import ssl


SERVER_ADDRESS = 'localhost'
SERVER_PORT = 10001
file_path = os.path.dirname(os.path.abspath(__file__))+'/' 
logging.basicConfig(level=logging.DEBUG)

class HttpsServer(BaseHTTPRequestHandler): 

    def set_response(self):
        self.send_response(200)
        self.send_header('content-type', 'text/html')
        self.end_headers()


    def do_GET(self):
        
        logging.info("GET request, \nPath: {0}\nHeaders:\n{1}\n".format(str(self.path), str(self.headers)))
        self.set_response()
        self.wfile.write("GET request for {0}".format(self.path).encode('utf-8'))
    

    def do_POST(self):
        print("---------------------------------------:  ",self.responses)
        content_length = int(self.headers['Content-Length'])
        data = self.rfile.read(content_length)
        logging.info("POST request,\nPath: {0}\nHeaders:\n{1}\n\nBody:\n\n{2}\n".format(
                str(self.path), str(self.headers), data.decode('utf-8')))
        self.set_response()
        self.wfile.write("POST request for {0}".format(self.path).encode('utf-8'))
        data = data.decode('utf-8')
        # self.send_to_rabbit(data)
        return data

    def send_to_rabbit(self,data):
        import stomp_rabbit
        to_rabbit = stomp_rabbit.ToRabbit()
        to_rabbit.connection(username='guest', password='guest')
        to_rabbit.send_to_queue(destination="test3", data_to_send=data)


def generate_selfsigned_certificate():
        attributes = "'/C=SN/ST=Senegal/L=Dakar/O=KebLink/OU=Dev Department/CN=www.keblink.com'"
        try:
            openssl_command = 'openssl req -newkey rsa:4096 -x509 -sha256 -days 3650 -nodes -out '+ file_path +'ssl_cert.crt -keyout '+ file_path +'ssl_key.key -subj ' + attributes + ''
            os.system(openssl_command)
        except Exception as e:
            logging.exception("ERROR DURING CERTIFICATE GENERATION: ", e)


def start_server(handler_class=HttpsServer, server_class=HTTPServer ):
    logging.basicConfig(level=logging.DEBUG)
    server_address = (SERVER_ADDRESS,SERVER_PORT) 
    server_ = server_class(server_address,handler_class)
    
    server_.socket = ssl.wrap_socket(server_.socket, server_side=True,certfile=file_path+"ssl_cert.crt", keyfile=file_path+"ssl_key.key")
    logging.info('Server_started at https://{0}:{1}'.format(SERVER_ADDRESS,SERVER_PORT))
    try:
        server_.serve_forever()
    except Exception as e:
        logging.exception("AN ERROR OCCURRED: ",e)
        server_.server_close()

def main():
    try:
        #  httpsServer = HttpsServer()
        generate_selfsigned_certificate()
        start_server(handler_class=HttpsServer)
    except Exception as e:
        logging.exception("AN ERROR OCCURRED: ",e)


if __name__ == "__main__":
    main()
    