from boofuzz import *

s_initialize('grammar')
s_static("HELLO\r\n")
s_static("PROCESS")
s_delim(" ")
s_string("AAAA")
s_static("\r\n")

target = Target(SocketConnection(host="127.0.0.1", port=4444))
sess = sessions.Session(session_filename="example_server.session", sleep_time=2)
sess.add_target(target)

sess.connect(s_get('grammar'))
sess.fuzz()
