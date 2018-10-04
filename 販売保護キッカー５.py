# coding:utf-8
#from linepy import *
from LineAPI.linepy import *
import random, requests, shutil, codecs, json, random, os
yukino_1 = LINE('tinkow@sute.jp','1018abc',appName='CHROMEOS\t2.1.5\tChrome_OS\t1')
yukino_2 = LINE('cecec@sute.jp','1018abc',appName='CHROMEOS\t2.1.5\tChrome_OS\t1')
yukino_3 = LINE('nnnnn1@sute.jp','1018abc',appName='CHROMEOS\t2.1.5\tChrome_OS\t1')
yukino_4 = LINE('dsdsd@sute.jp','1018abc',appName='CHROMEOS\t2.1.5\tChrome_OS\t1')
yukono_5 = LINE('arara@sute.jp','1018abc',appName='CHROMEOS\t2.1.5\tChrome_OS\t1')

tracer = OEPoll(yukino_1)
bots = [yukino_1, yukino_2, yukino_3, yukino_4]
kickers = [yukino_2, yukino_3]
yukino_1Mid = yukino_1.getProfile().mid
kickerMids = [yukino_2.getProfile().mid, yukino_3.getProfile().mid, yukino_4.getProfile().mid, yukono_5.getProfile().mid]
botMids = [yukino_1.getProfile().mid, yukino_2.getProfile().mid, yukino_3.getProfile().mid, yukino_4.getProfile().mid, yukono_5.getProfile().mid]
yukino_2Mid = yukino_2.getProfile().mid
yukino_3Mid = yukino_3.getProfile().mid
yukino_4Mid = yukino_4.getProfile().mid
yukino_5Mid = yukono_5.getProfile().mid
protect = {
    'normalProtect' : {},
    'groupName' : {},
    'groupPicture' : {},
    'groupUrl' : {},
    'blackUsers' : {},
    'whiteUsers' : {}
}


admins = ["u607b10261fdf476adeaf55ebddae2eb4","uc826d3bf17da72b21215836b0abc1acd"]
readData = codecs.open('./normalProtect.json', 'r', 'utf-8')
protect['normalProtect'] = json.load(readData)

readData = codecs.open('./groupName.json', 'r', 'utf-8')
protect['groupName'] = json.load(readData)

readData = codecs.open('./groupPicture.json', 'r', 'utf-8')
protect['groupPicture'] = json.load(readData)

readData = codecs.open('./groupUrl.json', 'r', 'utf-8')
protect['groupUrl'] = json.load(readData)

readData = codecs.open('./blackUsers.json', 'r', 'utf-8')
protect['blackUsers'] = json.load(readData)

readData = codecs.open('./whiteUsers.json', 'r', 'utf-8')
protect['whiteUsers'] = json.load(readData)

profile = yukino_1.getProfile()
helptext = "保護BOTのコマンド一覧だよ。上手く使ってね♪\n" \
            "★/mid✩୭⋆*✦*⋆୭*✩自分のmidを提示させる事が可能\n" \
            "★/gid✩୭⋆*✦*⋆୭*✩このグループのgidを提示させる事が可能\n" \
            "★/ginfo✩୭⋆*✦*⋆୭*✩グループの状態を提示させる事が可能n" \
            "★/info✩୭⋆*✦*⋆୭*✩このBOTの情報を提示させる事が可能\n" \
            "★/保護 オン✩୭⋆*✦*⋆୭*✩このグループの保護機能をオンにさせる事が可能\n" \
            "★/保護 オフ✩୭⋆*✦*⋆୭*✩このグループの保護機能をオフにさせる事が可能\n" \
            "★/保護 名前 オン✩୭⋆*✦*⋆୭*✩このグループ名の保護機能をオンにさせる事が可能\n" \
            "★/保護 名前 オフ✩୭⋆*✦*⋆୭*✩このグループ名の保護機能をオフにさせる事が可能\n" \
            "★/保護 画像 オン✩୭⋆*✦*⋆୭*✩このグループ画像の保護機能をオフにさせる事が可能\n" \
            "★/保護 画像 オフ✩୭⋆*✦*⋆୭*✩このグループ画像の保護機能をオフにさせる事が可能\n" \
            "★/保護 url オン✩୭⋆*✦*⋆୭*✩このグループurlの保護機能をオンにさせる事が可能\n" \
            "★/保護 url オフ✩୭⋆*✦*⋆୭*✩このグループurlの保護機能をオフにさせる事が可能\n" \
			"★/bye✩୭⋆*✦*⋆୭*✩このグループから保護BOTを退出させる事が可能\n" \
			"このBOTの使用者になりたい方は下記を追加してください\n\nhttp://line.me/ti/p/%40tuc0263b" 
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
                    if msg._from in protect['whiteUsers']:
                        for i in bots:
                            i.leaveGroup(msg.to)
                elif msg.text == "/help":
                    yukino_1.sendMessage(msg.to, helptext)
                elif msg.text.startswith('addwhite'):
                    yukino_1.sendMessage(msg.to, json.loads(msg.contentMetadata['MENTION'])['MENTIONEES'][0]['M'])
                    whiteUserMid = json.loads(msg.contentMetadata['MENTION'])['MENTIONEES'][0]['M']
                    if whiteUserMid in protect['whiteUsers']:
                        yukino_1.sendMessage(msg.to, "このユーザーはすでにホワイトリストに登録されています。")
                    else:
                        protect['whiteUsers'][whiteUserMid] = True
                        f = codecs.open('./whiteUsers.json','w','utf-8')
                        json.dump(protect['whiteUsers'], f, sort_keys=True, indent=4,ensure_ascii=False)
                        yukino_1.sendMessage(msg.to, "ホワイトリストに追加しました！")
                elif msg.text == "/保護 オン":
                    if msg._from in protect['whiteUsers']:
                        if msg.to in protect['normalProtect']:
                            yukino_1.sendMessage(msg.to, "保護機能はすでに有効になっています。")
                        else:
                            protect['normalProtect'][msg.to] = True
                            readData = codecs.open('./normalProtect.json','w','utf-8')
                            json.dump(protect['normalProtect'], readData, sort_keys=True, indent=4, ensure_ascii=False)
                            yukino_1.sendMessage(msg.to, "保護機能を有効にしました。")
                    elif msg._from in admins:
                        if msg.to in protect['normalProtect']:
                            yukino_1.sendMessage(msg.to, "保護機能はすでに有効になっています。")
                        else:
                            protect['normalProtect'][msg.to] = True
                            readData = codecs.open('./normalProtect.json','w','utf-8')
                            json.dump(protect['normalProtect'], readData, sort_keys=True, indent=4, ensure_ascii=False)
                            yukino_1.sendMessage(msg.to, "保護機能を有効にしました。")
                elif msg.text == "/保護 オフ":
                    if msg._from in protect['whiteUsers']:
                        if msg.to in protect['normalProtect']:
                            del protect['normalProtect'][msg.to]
                            readData = codecs.open('./normalProtect.json','w','utf-8')
                            json.dump(protect['normalProtect'], readData, sort_keys=True, indent=4, ensure_ascii=False)
                            yukino_1.sendMessage(msg.to, "保護機能を解除しました。")
                        else:
                            yukino_1.sendMessage(msg.to, "保護機能はすでに無効になっています。")
                    elif msg._from in admins:
                        if msg.to in protect['normalProtect']:
                            del protect['normalProtect'][msg.to]
                            readData = codecs.open('./normalProtect.json','w','utf-8')
                            json.dump(protect['normalProtect'], readData, sort_keys=True, indent=4, ensure_ascii=False)
                            yukino_1.sendMessage(msg.to, "保護機能を解除しました。")
                        else:
                            yukino_1.sendMessage(msg.to, "保護機能はすでに無効になっています。")
                elif msg.text == "/保護 名前 オン":
                    if msg._from in protect['whiteUsers']:
                        if msg.to in protect['groupName']:
                            yukino_1.sendMessage(msg.to, "グループ名の保護機能はすでに有効になっています。")
                        else:
                            protect['groupName'][msg.to] = yukino_1.getGroup(msg.to).name
                            f=codecs.open('./groupName.json','w','utf-8')
                            json.dump(protect['groupName'], f, sort_keys=True, indent=4,ensure_ascii=False)
                            yukino_1.sendMessage(msg.to, "グループ名の保護機能を有効にしました。")
                    elif msg._from in admins:
                        if msg.to in protect['groupName']:
                            yukino_1.sendMessage(msg.to, "グループ名の保護機能はすでに有効になっています。")
                        else:
                            protect['groupName'][msg.to] = yukino_1.getGroup(msg.to).name
                            f=codecs.open('./groupName.json','w','utf-8')
                            json.dump(protect['groupName'], f, sort_keys=True, indent=4,ensure_ascii=False)
                            yukino_1.sendMessage(msg.to, "グループ名の保護機能を有効にしました。。")
                elif msg.text == "/保護 名前 オフ":
                    if msg._from in protect['whiteUsers']:
                        if msg.to in protect['groupName']:
                            del protect['groupName'][msg.to]
                            readData = codecs.open('./groupName.json','w','utf-8')
                            json.dump(protect['groupName'], readData, sort_keys=True, indent=4, ensure_ascii=False)
                            yukino_1.sendMessage(msg.to, "グループ名の保護機能を解除しました。")
                        else:
                            yukino_1.sendMessage(msg.to, "グループ名の保護機能はすでに無効になっています。")
                    elif msg._from in admins:
                        if msg.to in protect['groupName']:
                            del protect['groupName'][msg.to]
                            readData = codecs.open('./groupName.json','w','utf-8')
                            json.dump(protect['groupName'], readData, sort_keys=True, indent=4, ensure_ascii=False)
                            yukino_1.sendMessage(msg.to, "グループ名の保護機能を解除しました。")
                        else:
                            yukino_1.sendMessage(msg.to, "グループ名の保護機能はすでに無効になっています。")
                elif msg.text == "/保護 画像 オン":
                    if msg._from in protect['whiteUsers']:
                        if msg.to in protect['groupPicture']:
                            yukino_1.sendMessage(msg.to, "グループ画像の保護機能はすでに有効になっています。")
                        else:
                            try:
                                imageName = random_string(10) + ".png"
                                download_img("http://dl.profile.line-cdn.net/"+yukino_1.getGroup(msg.to).pictureStatus, imageName)
                                protect['groupPicture'][msg.to] = imageName
                                readData = codecs.open('./groupPicture.json', 'w', 'utf-8')
                                json.dump(protect['groupPicture'], readData, sort_keys=True, indent=4, ensure_ascii=False)
                                yukino_1.sendMessage(msg.to, "グループ画像の保護機能を有効にしました。")
                            except:
                                yukino_1.sendMessage(msg.to, "グループ画像が設定されていません。\n設定してからこのコマンドを実行してください。")
                    elif msg._from in admins:
                        if msg.to in protect['groupPicture']:
                            yukino_1.sendMessage(msg.to, "グループ画像の保護機能はすでに有効になっています。")
                        else:
                            try:
                                imageName = random_string(10) + ".png"
                                download_img("http://dl.profile.line-cdn.net/"+yukino_1.getGroup(msg.to).pictureStatus, imageName)
                                protect['groupPicture'][msg.to] = imageName
                                readData = codecs.open('./groupPicture.json', 'w', 'utf-8')
                                json.dump(protect['groupPicture'], readData, sort_keys=True, indent=4, ensure_ascii=False)
                                yukino_1.sendMessage(msg.to, "グループ画像の保護機能を有効にしました。")
                            except:
                                yukino_1.sendMessage(msg.to, "グループ画像が設定されていません。\n設定してからこのコマンドを実行してください。")
                elif msg.text == "/保護 画像 オフ":
                    if msg._from in protect['whiteUsers']:
                        if msg.to in protect['groupPicture']:
                            imagePath = "./" + protect['groupPicture'][msg.to]
                            os.remove(imagePath)
                            del protect['groupPicture'][msg.to]
                            readData = codecs.open('./groupPicture.json','w','utf-8')
                            json.dump(protect['groupPicture'], readData, sort_keys=True, indent=4, ensure_ascii=False)
                            yukino_1.sendMessage(msg.to, "グループ画像の保護機能を解除しました。")
                        else:
                            yukino_1.sendMessage(msg.to, "グループ名の保護機能はすでに無効になっています。")
                    elif msg._from in admins:
                        if msg.to in protect['groupPicture']:
                            imagePath = "./" + protect['groupPicture'][msg.to]
                            os.remove(imagePath)
                            del protect['groupPicture'][msg.to]
                            readData = codecs.open('./groupPicture.json','w','utf-8')
                            json.dump(protect['groupPicture'], readData, sort_keys=True, indent=4, ensure_ascii=False)
                            yukino_1.sendMessage(msg.to, "グループ画像の保護機能を解除しました。")
                        else:
                            yukino_1.sendMessage(msg.to, "グループ名の保護機能はすでに無効になっています。")
                elif msg.text == "/保護 url オン":
                    if msg._from in protect['whiteUsers']:
                        if msg.to in protect['groupUrl']:
                            yukino_1.sendMessage(msg.to, "グループurlの保護機能はすでに有効になっています。")
                        else:
                            protect['groupUrl'][msg.to] = True
                            readData = codecs.open('./groupUrl.json', 'w', 'utf-8')
                            json.dump(protect['groupUrl'], readData, sort_keys=True, indent=4, ensure_ascii=False)
                            yukino_1.sendMessage(msg.to, "グループurlの保護機能を有効にしました。")
                            G =yukino_1.getGroup(msg.to)
                            G.preventJoinByTicket = True
                            yukino_1.updateGroup(G)
                    elif msg._from in admins:
                        if msg.to in protect['groupUrl']:
                            yukino_1.sendMessage(msg.to, "グループurlの保護機能はすでに有効になっています。")
                        else:
                            protect['groupUrl'][msg.to] = True
                            readData = codecs.open('./groupUrl.json', 'w', 'utf-8')
                            json.dump(protect['groupUrl'], readData, sort_keys=True, indent=4, ensure_ascii=False)
                            yukino_1.sendMessage(msg.to, "グループurlの保護機能を有効にしました。")
                            G =yukino_1.getGroup(msg.to)
                            G.preventJoinByTicket = True
                            yukino_1.updateGroup(G)
                elif msg.text == "/保護 url オフ":
                    if msg._from in protect['whiteUsers']:
                        if msg.to in protect['groupUrl']:
                            del protect['groupUrl'][msg.to]
                            readData = codecs.open('./groupUrl.json','w','utf-8')
                            json.dump(protect['groupUrl'], readData, sort_keys=True, indent=4, ensure_ascii=False)
                            yukino_1.sendMessage(msg.to, "グループurlの保護機能を解除しました。")
                        else:
                            yukino_1.sendMessage(msg.to, "グループurlの保護機能はすでに無効になっています。")
                    elif msg._from in admins:
                        if msg.to in protect['groupUrl']:
                            del protect['groupUrl'][msg.to]
                            readData = codecs.open('./groupUrl.json','w','utf-8')
                            json.dump(protect['groupUrl'], readData, sort_keys=True, indent=4, ensure_ascii=False)
                            yukino_1.sendMessage(msg.to, "グループurlの保護機能を解除しました。")
                        else:
                            yukino_1.sendMessage(msg.to, "グループurlの保護機能はすでに無効になっています。")
                elif msg.text == "/ginfo":
                    group = yukino_1.getGroup(msg.to)
                    md = "[グループ名]: " + group.name + "\n\n[gid]: " + group.id + "\n\n[アイコン画像]: \nhttp://dl.profile.line-cdn.net/" + group.pictureStatus
                    if group.preventedJoinByTicket is False: md += "\n\n招待URL: 許可中です\n"
                    else: md += "\n\n招待URL: 拒否中です\n"

                    if group.invitee is None: md += "\nメンバー数: " + str(len(group.members)) + "人\n招待中: 0人"
                    else: md += "\nメンバー数: " + str(len(group.members)) + "人\n招待中: " + str(len(group.invitee)) + "人"

                    if msg.to in protect['normalProtect']: md += "\n\n保護: オン"
                    else: md += "\n\n保護: オフ"

                    if msg.to in protect['groupUrl']: md += "\n\n保護 URL: オン"
                    else: md += "\n\n保護 URL: オフ"

                    if msg.to in protect['groupName']: md += "\n\n保護 グループ名: オン"
                    else: md += "\n\n保護 グループ名: オフ"

                    if msg.to in protect['groupPicture']: md += "\n\n保護 グループ画像: オン"
                    else: md += "\n\n保護 グループ画像: オフ"
                    yukino_1.sendMessage(msg.to, md)
                elif msg.text == "招待URL拒否":
                    group = yukino_1.getGroup(msg.to)
                    if group.preventedJoinByTicket == True:
                        yukino_1.sendMessage(msg.to, "既に拒否されています")
                    else:
                        group.preventedJoinByTicket = True
                        yukino_1.updateGroup(group)
                        yukino_1.sendMessage(msg.to, "URL招待を拒否しました")
                elif msg.text == "招待URL許可":
                    group = client.getGroup(msg.to)
                    if group.preventedJoinByTicket == False:
                        yukino_1.sendMessage(msg.to, "既に許可されています。")
                    else:
                        if msg.to in protect['groupUrl']:
                            yukino_1.sendMessage(msg.to, "招待URLの設定変更が禁止されているので作成できません。\n保護 URL オフを実行してください。")
                        else:
                            group.preventedJoinByTicket = False
                            client.updateGroup(group)
                            yukino_1.sendMessage(msg.to, "URL招待を許可しました。")
                
            except Exception as error:
                print(error)
    except Exception as error:
        print(error) 
tracer.addOpInterrupt(26, RECEIVE_MESSAGE)
def NOTIFIED_KICKOUT_FROM_GROUP(op):
    print(op)
    try:
        if op.param1 in protect['normalProtect']:
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
                    f=codecs.open('./blackUsers.json','w','utf-8')
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
                    f=codecs.open('./blackUsers.json','w','utf-8')
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
                    f=codecs.open('./blackUsers.json','w','utf-8')
                    json.dump(protect['blackUsers'], f, sort_keys=True, indent=4,ensure_ascii=False)
    except Exception as error:
        print(error)
tracer.addOpInterrupt(19, NOTIFIED_KICKOUT_FROM_GROUP)
def NOTIFIED_INVITE_INTO_GROUP(op):
    try:
        if profile.mid in op.param3:
            if op.param2 in botMids:
                return
            elif op.param2 in protect['whiteUsers']:
                yukino_1.acceptGroupInvitation(op.param1)
                yukino_1.sendMessage(op.param1,"よろしくね！！このグループを保護BOTです。\n使用方法はは「/help」で確認してください♪")
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
            elif op.param2 in admins:
                yukino_1.acceptGroupInvitation(op.param1)
                yukino_1.sendMessage(op.param1,"よろしくね！！このグループを保護BOTです。\n使用方法はは「/help」で確認してください♪")
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
                        f=codecs.open('./blackUsers.json','w','utf-8')
                        json.dump(protect['blackUsers'], f, sort_keys=True, indent=4,ensure_ascii=False)
    except Exception as error:
        print(error)

tracer.addOpInterrupt(11,NOTIFIED_UPDATE_GROUP)
while True:
    tracer.trace()