#!/usr/bin/env python3

import ts3

# TODO: Add config so all this crap isn't hard coded

__all__ = ["KelnetBot"]
timeout = 1800000

def bot_main(ts3conn):
    ts3conn.servernotifyregister(event="server")
    ts3conn.clientupdate(client_nickname="KelnetBot")
    cl = ts3conn.clientlist(away=True,times=True,info=True)
    for client in cl:
        info = ts3conn.clientinfo(clid=client['clid'])
        sg = info[0]['client_servergroups']
        if sg == '6' or sg == '40' or sg == '12':
            ts3conn.sendtextmessage(targetmode=1, target=client['clid'], msg="KelnetBot has started successfully")
    
    while True:
        
        cl = ts3conn.clientlist(away=True,times=True,info=True)
        for client in cl:
            try:
                info = ts3conn.clientinfo(clid=client['clid'])
            except TS3ParserError as e:
                print("Unable to parse client data: {}".format(e))
            if int(client['client_idle_time']) >= timeout and info[0]['cid'] != '177':
                print("Moved client {} to AFK channel".format(client['client_nickname']))
                ts3conn.clientmove(cid='177', clid=client['clid'])

        try:
            event = ts3conn.wait_for_event(timeout=500)
        except ts3.query.TS3TimeoutError:
            pass
        else:
            try:
                if event[0]['reasonid'] == "0":
                    nick = event[0]['client_nickname']
                    print("Client {} has joined the server.".format(event[0]['client_nickname']))
                    dbinfo = ts3conn.clientdbinfo(cldbid=event[0]['client_database_id'])
                    if nick == "SAY WHAT":
                        ts3conn.clientpoke(clid=event[0]["clid"], msg="I SWEAR TO GOD, TIM")
                    if nick == "Chaosthecrow":
                        ts3conn.clientpoke(clid=event[0]["clid"], msg="Whore")
                    if dbinfo[0]['client_totalconnections'] == "1":
                        print("Client {} has joined for the first time.".format(event[0]['client_nickname']))
                        ts3conn.clientpoke(clid=event[0]["clid"], msg="Welcome to the KelnetGaming TS3 server. You move, you must be promoted. Poke an admin to get promoted.")
            except Exception as e:
                print("Unable to process event: {}".format(e))

with ts3.query.TS3Connection('kelnet.org') as ts3conn:
    ts3conn.login(client_login_name='serveradmin', client_login_password='xxxxx')
    ts3conn.use(sid=1)
    bot_main(ts3conn)
