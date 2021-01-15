import socket
from _thread import *
import pickle
from game import Game
import question

#   ip serveru (v uvozovkách)
server = "192.168.2.104"
port = 5555

#   Pro ipv4
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#   Použití ip a portu
try:
    s.bind((server, port))
except socket.error as e:
    str(e)

#   Mohou se připojit 2 klienti
s.listen(2)
print("Waiting for a connection, Server Started")

connected = set()
games = {}
idCount = 0


def adding_score(player, score, game):
    r = range(6)
    for i in r:
        if i * 1000 == score:
            print(score)
            game.add_score(player, score)


#   Běží v pozadí, mezitím co se stále hledá další připojení (běží while a zároveň funkce)
def threaded_client(conn, p, gameId):
    global idCount
    #   Poslání informací o klientovi jaký je hráč player1 / player2
    conn.send(str.encode(str(p)))

    reply = ""
    #   Běží stále, mezitím co je klient připojený
    while True:
        try:
            #   4096 - bity, které se přijímají (když jsou errory, stačí navýšit)
            data = conn.recv(4096).decode()

            #   kontroluje se jestli hra stále existuje, protože když se hráči odpojí, hra (s ID) se smaže
            if gameId in games:
                game = games[gameId]

                #   Pokud nepřichází žádné data
                if not data:
                    break
                else:
                    #   resetuje p1 a p2 Went
                    if data == "reset":
                        game.resetWent()
                    elif data == "change":
                        game.change_player_turn()
                    elif data == "questionDisplay":
                        game.change_question_display()
                    elif data[0] == "1":
                        adding_score(1, int(data[1:]), game)
                    elif data[0] == "2":
                        adding_score(2, int(data[1:]), game)
                    elif data[0] == "b":
                        game.change_current_q(str(data[4:]), str(data[3]))
                    elif data[0] == "s":
                        game.button_display(data[2], data[3])
                    # elif data == "end":
                    #     game.end()
                    elif data != "get":
                        game.play(p, data)

                    conn.sendall(pickle.dumps(game))
            else:
                break
        except:
            break

    print("Lost connection")
    try:
        #   Smaže se hra (s ID)
        del games[gameId]
        print("Closing Game", gameId)
    except:
        pass
    idCount -= 1
    conn.close()



#   Sleduje jestli se někdo připojil
while True:
    conn, addr = s.accept()
    print("Connected to:", addr)

    #   Počet připojených klientů
    idCount += 1
    #   player1
    p = 0
    #   Každých 2 připojených klientů se zvětší gameId o 1
    gameId = (idCount - 1)//2
    if idCount % 2 == 1:
        games[gameId] = Game(gameId)
        print("Creating a new game...")
    else:
        games[gameId].ready = True
        #   player2
        p = 1


    start_new_thread(threaded_client, (conn, p, gameId))
