from socket import AF_INET, socket, SOCK_STREAM


PORT=8000
SERVER = '127.0.0.1' #PORT và SERVER IP Address

#hàm xử lí request nhận được
def Handle_Client_Request(connection):
    request = connection.recv(1024)             #nhận request
    if request:
        request = request.decode('utf-8')       #decode to UTF-8
    else:                                       #không nhận được request in thông báo rồi thoát ra
        print("We Not received any request\n")
        return

    print("Client request: \n" + request)

    str_list = request.split(' ')   #tách chuỗi để xử lý
    method = str_list[0]            #method là loại request
    
    if method == "GET":             #xử lí method GET
        req_file = str_list[1]      #tên file
        req_file = req_file.lstrip('/')
        req_file = req_file.replace("%20", " ")
        if (req_file == ''):        #nếu không có tên file thì gán là index.html
            req_file = 'index.html'

        file = open(req_file, 'rb')         #mở file 
        response = file.read()              #đọc nội dung file vào response
        file.close()
        header = "HTTP/1.1 200 OK\n"        #thêm header của response
        if req_file.endswith(".html"):      
             header += "Content-Type: text/html\n\n"
        elif req_file.endswith(".css"):
             header += "Content-Type: text/css\n\n"
        else:
             header += "Content=Type: */*\n\n"

        final_res = header.encode('utf-8')   
        final_res += response                   
        connection.send(final_res)              #gửi response cho Client

    elif method == "POST":                          #xử lí method POST
        str_split = request.split('\n')             #tách chuỗi lấy username và password
        loginInfo = str_split[-1]
        username = loginInfo.split('&')[0]
        password = loginInfo.split('&')[1]
        username = username[9:]
        password = password[9:]
        if username == "admin" and password == "admin":                         # kiểm tra password, đúng -> truy cập trang info
            header = "HTTP/1.1 301 Moved Permanently\nLocation: /info.html\n"   #header của HTTP Redirection
            connection.send(header.encode('utf-8'))  
        else:                 #password sai -> truy cập trang báo lỗi 404
            header = "HTTP/1.1 404 Not Found\n\n"
            file = open("404.html", "rb")
            response = file.read()
            file.close()
            final_res = header.encode('utf-8')
            final_res += response
            connection.send(final_res)
#Tạo HostServer 
def HostServer():
    HOST = socket(AF_INET, SOCK_STREAM)     #Tạo socket
    
    HOST.bind((SERVER, PORT))               #gán IP Address và PORT
    HOST.listen(1)                          #lắng nghe kết nối
    print("Server is listening at http://" + SERVER + ":" + str(PORT))   
    while (1):
            connection, address = HOST.accept()         #chấp nhận kết nối từ Client
            print("Connected to " + str(address))
            Handle_Client_Request(connection)           #gọi hàm xử lí request từ client
            connection.close()                          #đóng kết nối đến Client 
 
    print("Server is closing...")
    HOST.close()    #Đóng HostServer

HostServer()    
