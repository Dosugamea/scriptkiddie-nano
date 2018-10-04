# coding:utf-8
from linepy import *
import random, requests, shutil, codecs, json, random, os
yukino_1 = LINE()
yukino_2 = LINE()
yukino_3 = LINE()

tracer = OEPoll(yukino_1)
bots = [yukino_1, yukino_2, yukino_3]
kickers = [yukino_2, yukino_3]
yukino_1Mid = yukino_1.getProfile().mid
kickerMids = [yukino_2.getProfile().mid, yukino_3.getProfile().mid]
botMids = [yukino_1.getProfile().mid, yukino_2.getProfile().mid, yukino_3.getProfile().mid]
yukino_2Mid = yukino_2.getProfile().mid
yukino_3Mid = yukino_3.getProfile().mid
protect = {
    'kickGroup' : {}, 
    'normalProtect' : {},
    'groupName' : {},
    'groupPicture' : {},
    'groupUrl' : {},
    'blackUsers' : {},
    'whiteUsers' : {}
}


admins = ["",""]
readData = codecs.open('blackUsers.json', 'r', 'utf-8')
protect['blackUsers'] = json.load(readData)
profile = yukino_1.getProfile()
helptext = "--このbotヘルプ--\n" \
            "/mid...midを送信します。\n" \
            "/gid...gidを送信します。\n" \
            "/ginfo...グループの情報を表示します。\n" \
            "/保護 オン...保護機能をオンにします。\n" \
            "/保護 オフ...保護機能をオフにします。"
print(protect)
print("success")
def download_img(url, file_name):
    r = requests.get(url, stream=True)
    if r.status_code == 200:
        with open(file_name, 'wb') as f:
            r.raw.decode_content = True
            shutil.copyfileobj(r.raw, f)
def random_string(length, seq='0123456789abcdefghijklmnopqrstuvwxyz'):
    sr = random.SystemRandom()
    return ''.join([sr.choice(seq) for i in range(length)])
    
def RECEIVE_MESSAGE(op):
    msg = op.message
    print(op)
    try:
        if 0 == msg.contentType:
            try:
                if msg.text == "/mid":
                    yukino_1.sendMessage(msg.to, msg._from)
                elif msg.text == "/gid":
                    yukino_1.sendMessage(msg.to, msg.to)
                elif msg.text == "/bye":
                    for i in bots:
                        i.leaveGroup(msg.to)
                elif msg.text == "/help":
                    yukino_1.sendMessage(msg.to, helptext)
                elif msg.text == "/保護 オン":
                    if msg.to in protect['kickGroup']:
                        if msg.to in protect['normalProtect']:
                            yukino_1.sendMessage(msg.to, "保護機能はすでに有効になっています。")
                        else:
                            protect['normalProtect'][msg.to] = True
                            readData = codecs.open('normalProtect.json','w','utf-8')
                            json.dump(protect['normalProtect'], readData, sort_keys=True, indent=4, ensure_ascii=False)

                            protect['kickGroup'][msg.to] = True
                            readData = codecs.open('kickGroup.json','w','utf-8')
                            json.dump(protect['kickGroup'], readData, sort_keys=True, indent=4, ensure_ascii=False)
                            yukino_1.sendMessage(msg.to, "保護機能を有効にしました。")
                elif msg.text == "/保護 オフ":
                    if msg.to in protect['kickGroup']:
                        del protect['kickGroup'][msg.to]
                        readData = codecs.open('kickGroup.json','w','utf-8')
                        json.dump(protect['kickGroup'], readData, sort_keys=True, indent=4, ensure_ascii=False)
                    if msg.to in protect['normalProtect']:
                        del protect['normalProtect'][msg.to]
                        readData = codecs.open('normalProtect.json','w','utf-8')
                        yukino_1.sendMessage(msg.to, "保護機能を解除しました。")
                    else:
                        yukino_1.sendMessage(msg.to, "保護機能はすでに無効になっています。")
            except Exception as error:
                print(error)
    except Exception as error:
        print(error) 
tracer.addOpInterrupt(26, RECEIVE_MESSAGE)
def NOTIFIED_KICKOUT_FROM_GROUP(op):
    print(op)
    try:
        if op.param1 in protect['kickGroup']:
            if op.param2 in kickerMids:
                return
            elif op.param2 in protect['whiteUsers']:
                if op.param3 in kickerMids:
                    try:
                        yukino_1.inviteIntoGroup(op.param1, [op.param3])
                        if op.param3 in yukino_2Mid:
                            yukino_2.acceptGroupInvitation(op.param1)
                        elif op.param3 in yukino_3Mid:
                            yukino_3.acceptGroupInvitation(op.param1)
                    except:
                        groupInfomation = yukino_1.getGroup(op.param1)
                        if groupInfomation.preventedJoinByTicket == False:
                            Ticket = yukino_1.reissueGroupTicket(op.param1)
                            for i in bots:
                                i.acceptGroupInvitationByTicket(op.param1, Ticket)
                        else:
                            groupInfomation.preventedJoinByTicket = False
                            yukino_1.updateGroup(groupInfomation)
                            Ticket = yukino_1.reissueGroupTicket(op.param1)
                            for i in bots:
                                i.acceptGroupInvitationByTicket(op.param1, Ticket)
                elif op.param3 in yukino_1Mid:
                    Kicker = random.choice(kickers)
                    try:
                        Kicker.inviteIntoGroup(op.param1, [op.param3])
                        yukino_1.acceptGroupInvitation(op.param1)
                    except:
                        groupInfomation = yukino_1.getGroup(op.param1)
                        if groupInfomation.preventedJoinByTicket == False:
                            Ticket = yukino_1.reissueGroupTicket(op.param1)
                            for i in bots:
                                i.acceptGroupInvitationByTicket(op.param1, Ticket)
                        else:
                            groupInfomation.preventedJoinByTicket = False
                            yukino_1.updateGroup(groupInfomation)
                            Ticket = yukino_1.reissueGroupTicket(op.param1)
                            for i in bots:
                                i.acceptGroupInvitationByTicket(op.param1, Ticket)
            elif op.param3 in kickerMids:
                try:
                    yukino_1.inviteIntoGroup(op.param1, [op.param3])
                    if op.param3 in yukino_2Mid:
                        yukino_2.acceptGroupInvitation(op.param1)
                    elif op.param3 in yukino_3Mid:
                        yukino_3.acceptGroupInvitation(op.param1)
                    elif op.param3 in yukino_4Mid:
                        yukino_4.acceptGroupInvitation(op.param1)
                    else:
                        yukino_5.acceptGroupInvitation(op.param1)
                except:
                    groupInfomation = yukino_1.getGroup(op.param1)
                    if groupInfomation.preventedJoinByTicket == False:
                        Ticket = yukino_1.reissueGroupTicket(op.param1)
                        for i in bots:
                            i.acceptGroupInvitationByTicket(op.param1, Ticket)
                    else:
                        groupInfomation.preventedJoinByTicket = False
                        yukino_1.updateGroup(groupInfomation)
                        Ticket = yukino_1.reissueGroupTicket(op.param1)
                        for i in bots:
                            i.acceptGroupInvitationByTicket(op.param1, Ticket)
                try:
                    Kicker = random.choice(kickers)
                    Kicker.kickoutFromGroup(op.param1, [op.param2])
                except:
                    pass
                if op.param2 in protect['blackUsers']:
                    pass
                else:
                    protect['blackUsers'][op.param2] = True
                    f=codecs.open('blackUsers.json','w','utf-8')
                    json.dump(protect['blackUsers'], f, sort_keys=True, indent=4,ensure_ascii=False)
            elif op.param3 in yukino_1Mid:
                K = random.choice(kickers)
                K.kickoutFromGroup(op.param1, [op.param2])
                try:
                    K.inviteIntoGroup(op.param1, [op.param3])
                    yukino_1.acceptGroupInvitation(op.param1)
                except:
                    groupInfomation = yukino_2.getGroup(op.param1)
                    if groupInfomation.preventedJoinByTicket == False:
                        Ticket = yukino_2.reissueGroupTicket(op.param1)
                        for i in bots:
                            i.acceptGroupInvitationByTicket(op.param1, Ticket)
                    else:
                        groupInfomation.preventedJoinByTicket = False
                        yukino_2.updateGroup(groupInfomation)
                        Ticket = yukino_1.reissueGroupTicket(op.param1)
                        for i in bots:
                            i.acceptGroupInvitationByTicket(op.param1, Ticket)
                if op.param2 in protect['blackUsers']:
                    pass
                else:
                    protect['blackUsers'][op.param2] = True
                    f=codecs.open('blackUsers.json','w','utf-8')
                    json.dump(protect['blackUsers'], f, sort_keys=True, indent=4,ensure_ascii=False)
            else:
                try:
                    yukino_3.kickoutFromGroup(op.param1, [op.param2])
                except:
                    try:
                        yukino_2.kickoutFromGroup(op.param1, [op.param2])
                    except Exception as error:
                        print(error)
                yukino_3.inviteIntoGroup(op.param1, [op.param3])
                if op.param2 in protect['blackUsers']:
                    pass
                else:
                    protect['blackUsers'][op.param2] = True
                    f=codecs.open('blackUsers.json','w','utf-8')
                    json.dump(protect['blackUsers'], f, sort_keys=True, indent=4,ensure_ascii=False)
    except Exception as error:
        print(error)
tracer.addOpInterrupt(19, NOTIFIED_KICKOUT_FROM_GROUP)
def NOTIFIED_INVITE_INTO_GROUP(op):
    try:
        if profile.mid in op.param3:
            if op.param2 in botMids:
                return
            else:
                yukino_1.acceptGroupInvitation(op.param1)
                yukino_1.sendMessage(op.param1,"保護botです。このグループを保護します。\n使い方は「/help」で確認してください。")
                try:
                    yukino_1.inviteIntoGroup(op.param1, kickerMids)
                    for i in bots:
                        i.acceptGroupInvitation(op.param1)
                except:
                    groupInfomation = yukino_1.getGroup(op.param1)
                    if groupInfomation.preventedJoinByTicket == False:
                        Ticket = yukino_1.reissueGroupTicket(op.param1)
                        for i in bots:
                            i.acceptGroupInvitationByTicket(op.param1, Ticket)
                    else:
                        groupInfomation.preventedJoinByTicket = False
                        yukino_1.updateGroup(groupInfomation)
                        Ticket = yukino_1.reissueGroupTicket(op.param1)
                        for i in bots:
                            i.acceptGroupInvitationByTicket(op.param1, Ticket)
                    G = yukino_1.getGroup(op.param1)
                    G.preventedJoinByTicket = True
                    yukino_1.updateGroup(G)
        elif op.param1 in protect['normalProtect']:
            Inviter = op.param3.replace("",',')
            InviterX = Inviter.split(",")
            matched_list = []
            for tag in protect['blackUsers']:
                matched_list+=filter(lambda str: str == tag, InviterX)
            if matched_list == []:
                pass
            else:
                yukino_1.cancelGroupInvitation(op.param1, matched_list)
                for i in bots:
                    i.kickoutFromGroup(op.param1,[op.param2])
    except Exception as error:
        print(error)
tracer.addOpInterrupt(13, NOTIFIED_INVITE_INTO_GROUP)
def NOTIFIED_UPDATE_GROUP(op):
    print(op)
    try:
        """
        op.param3
        1がグループ名
        2がグループ画像
        4がurl
        """
        if op.param3 == "1":
            if op.param1 in protect['groupName']:
                if op.param2 in botMids:
                    pass
                else:
                    groupInfomation = yukino_1.getGroup(op.param1)
                    groupInfomation.name = protect['groupName'][op.param1]
                    yukino_1.updateGroup(groupInfomation)
        elif op.param3 == "2":
            if op.param1 in protect['groupPicture']:
                if op.param2 in botMids:
                    pass
                else:
                    imagePath = "./" + protect['groupPicture'][op.param1]
                    yukino_1.updateGroupPicture(op.param1, imagePath)
        elif op.param3 == "4":
            if op.param1 in protect['groupUrl']:
                if op.param2 in botMids:
                    pass
                else:
                    groupInfomation = yukino_1.getGroup(op.param1)
                    groupInfomation.preventedJoinByTicket = True
                    yukino_1.updateGroup(groupInfomation)
                    if op.param2 in protect['blackUsers']:
                        pass
                    else:
                        protect['blackUsers'][op.param2] = True
                        f=codecs.open('blackUsers.json','w','utf-8')
                        json.dump(protect['blackUsers'], f, sort_keys=True, indent=4,ensure_ascii=False)
    except Exception as error:
        print(error)

tracer.addOpInterrupt(11,NOTIFIED_UPDATE_GROUP)
while True:
    tracer.trace()