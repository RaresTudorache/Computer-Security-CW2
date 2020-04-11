import sys
import os
from common import *
from const import *

dialog = Dialog('print')

flag = sys.argv[1]

#establish the connection
socket_alice, aes_alice = setup('alice', BUFFER_DIR, BUFFER_FILE_NAME)
os.rename(BUFFER_DIR + BUFFER_FILE_NAME, BUFFER_DIR + "BOB_BUFFER")
socket_bob, aes_bob = setup('bob', BUFFER_DIR, BUFFER_FILE_NAME)

#recieve message from Alice
received = receive_and_decrypt(aes_bob, socket_bob) 

dialog.chat('Alice said: "{}"'.format(received))

if flag == '--relay':
    reply  = received

if flag == '--break-heart':
    reply = BAD_MSG['alice']

if flag == '--custom':
    dialog.prompt('What would you like Alice to say to Bob?')
    reply = input()

#send message to Bob
encrypt_and_send(reply, aes_alice, socket_alice)
dialog.info('Message sent! Waiting for reply...')
#get message from Bob
received = receive_and_decrypt(aes_alice, socket_alice)
dialog.chat('Bob said: "{}"'.format(received))

if flag == '--custom':
    dialog.prompt('What would you like Bob to say to Alice?')
    reply = input()
else:
    reply = received

#send message to Alice
encrypt_and_send(reply, aes_bob, socket_bob)

#close the connection
tear_down(socket_alice, BUFFER_DIR, "BOB_BUFFER")
tear_down(socket_bob, BUFFER_DIR, BUFFER_FILE_NAME)

    

