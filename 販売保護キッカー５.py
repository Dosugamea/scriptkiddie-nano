# coding:utf-8
from LineAPI.hooks import HooksTracer
from collections   import OrderedDict
import random, requests, shutil, codecs, json, random, os

with open("Tokens.json","r",encoding="utf8") as f:
    tokens = json.loads(f.read(),object_pairs_hook=OrderedDict)
    
with open("Help.txt","r",encoding="utf8") as f:
    helpText = f.read()
    
yukino_1 = LINE(tokens["Main"],type="IOSIPAD")
yukino_2 = LINE(tokens["Sub1"],type="IOSIPAD")
yukino_3 = LINE(tokens["Sub2"],type="IOSIPAD")
yukino_4 = LINE(tokens["Sub3"],type="IOSIPAD")
yukino_5 = LINE(tokens["Sub4"],type="IOSIPAD")
tracer   = HooksTracer(yukino_1,prefix=["/"],db=None)


bots        = [yukino_1, yukino_2, yukino_3, yukino_4, yukino_5]
kickers     = [yukino_2, yukino_3, yukino_4]
botMids     = [b.getProfile().mid for b in bots]
kickerMids  = [k.getProfile().mid for k in kickers]

yukino_1Mid = yukino_1.getProfile().mid
yukino_2Mid = yukino_2.getProfile().mid
yukino_3Mid = yukino_3.getProfile().mid
yukino_4Mid = yukino_4.getProfile().mid
yukino_5Mid = yukino_5.getProfile().mid

'''
Initialize Area

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
'''

class FuncPs(object):
    def reTryInvite(self):
        cl = self.cl
        gr = cl.getGroup(gid)
        #DANGEROUS
        if gr.preventedJoinByTicket == False:
            Ticket = cl.reissueGroupTicket(gid)
            for i in bots:
                i.acceptGroupInvitationByTicket(gid, Ticket)
        else:
            groupInfomation.preventedJoinByTicket = False
            cl.updateGroup(groupInfomation)
            Ticket = yukino_1.reissueGroupTicket(gid)
            for i in bots:
                i.acceptGroupInvitationByTicket(gid, Ticket)

    def toggle(self,to,key):
        pass

class OpPs(object):
    @tracer.Operation(26)
    def RECIEVE_MESSAGE(self,cl,op):
        msg = op.message
        self.trace("Command",msg)
        
    @tracer.Operation(19)
    def NOTIFIED_KICKOUT_FROM_GROUP(self,cl,op):
        gid    = op.param1
        kicker = op.param2
        gotban = op.param3
        try:
            #保護対象であるなら
            if gid in protect['normalProtect']:
                #追い出したのがキッカーまたは ホワイトリストでなければ
                if kicker not in kickerMids and kicker not in whiteUsers:
                    #追い出されたのがBotならリストからそれを抜く
                    #追い出したキッカーを追い出す
                    #追い出された人を再招待
                    #ブラックリストに入ってなければ登録
                #ホワイトリストユーザーがキッカー/メイン垢を追い出してしまったなら
                if kicker in whiteUsers and gotban in botMids:
                    #追い出されたBotをリストから抜いて
                    #再招待
        except Exception as error:
            print(error)
        
    @tracer.Operation(13)
    def NOTIFIED_INVITE_INTO_GROUP(self,cl,op):
        gid        = op.param1
        inviter    = op.param2
        got_inv    = op.param3
        try:
            #自分のmid
            if yukino_1Mid in got_inv:
                #招待者がホワイトリストユーザー または 管理者
                if inviter in protect['whiteUsers'] or inviter in admins:
                    #招待受け入れ
                    cl.acceptGroupInvitation(op.param1)
                    cl.inviteIntoGroup(op.param1, kickerMids)
                        for i in bots:
                            try:
                                i.acceptGroupInvitation(op.param1)
                            except:
                                pass
                    cl.sendMessage(op.param1,"Hello! I'm group protect bot.\nYou can check my commands by '/help'♪")
            #招待保護中なら
            elif gid in protect['normalProtect']:
                gotinvs = op.param3.replace("",',').split(",")
                bl_usrs = [u for u in gotinvs if u in protect['blackUsers']]
                for b in bl_usrs:
                    cl.cancelGroupInvitation(op.param1, bl_usrs)
        except Exception as error:
            print(error)

    @tracer.Operation(11)
    def NOTIFIED_UPDATE_GROUP(self,cl,op):
        gid = op.param1
        usr = op.param2
        ctp = op.param3
        """
        ctp
        1: グループ名
        2: グル画像
        4: URL状態
        """
        try:
            #グループ名変更
            if ctp == "1":
                if gid in protect['groupName']:
                    if usr not in botMids:
                        gr = cl.getGroup(gid)
                        gr.name = protect['groupName'][gid]
                        cl.updateGroup(gr)
            #グループ画変更
            elif ctp == "2":
                if gid in protect['groupPicture']:
                    if usr not in botMids:
                        imagePath = "./" + protect['groupPicture'][gid]
                        cl.updateGroupPicture(gid, imagePath)
            #グループURL変更
            elif ctp == "4":
                if gid in protect['groupUrl']:
                    if usr not in botMids:
                        gr = cl.getGroup(gid)
                        gr.preventedJoinByTicket = True
                        cl.updateGroup(gr)
                        if usr not in protect['blackUsers']:
                            protect['blackUsers'][usr] = True
                            f=codecs.open('./blackUsers.json','w','utf-8')
                            json.dump(protect['blackUsers'], f, sort_keys=True, indent=4,ensure_ascii=False)
        except Exception as error:
            print(error)

class CmdPs(object):
    @tracer.Command()
    def hi(self,cl,msg):
        cl.replyMessage(msg,"Hi!")
        
    @tracer.Command()
    def mid(self,cl,msg):
        cl.replyMessage(msg,msg._from)
        
    @tracer.Command(sources=["Group"])
    def gid(self,cl,msg):
        cl.replyMessage(msg,msg.to)
        
    @tracer.Command(sources=["Group"],permissions=["Admin","White"])
    def bye(self,cl,msg):
        for i in self.bots:
            i.leaveGroup(msg.to)
    
    @tracer.Command()
    def help(self,cl,msg):
        cl.replyMessage(msg, self.helptext)
        
    @tracer.Command()
    def ginfo(self,cl,msg):
        group = cl.getGroup(msg.to)
        md =  "[グループ名]:\n" + group.name + "\n\n"
        md += "[gid]:\n" + group.id + "\n\n"
        md += "[アイコン画像]:\n" + "http://dl.profile.line-cdn.net/"
        md += group.pictureStatus + "\n\n"
        if group.preventedJoinByTicket:
            md += "\n\n招待URL: 拒否中です\n"
        else:
            md += "\n\n招待URL: 許可中です\n"
        md += "\nメンバー数: " + str(len(group.members)) + "人\n"
        if group.invitee is None:
            md += "招待中: 0人\n\n"
        else
            md += "招待中: " + str(len(group.invitee)) + "人\n\n"
        if msg.to in protect['normalProtect']:
            md += "\n\n保護: オン"
        else:
            md += "\n\n保護: オフ"
        if msg.to in protect['groupUrl']:
            md += "\n\n保護 URL: オン"
        else:
            md += "\n\n保護 URL: オフ"
        if msg.to in protect['groupName']:
            md += "\n\n保護 グループ名: オン"
        else:
            md += "\n\n保護 グループ名: オフ"
        if msg.to in protect['groupPicture']:
            md += "\n\n保護 グループ画像: オン"
        else:
            md += "\n\n保護 グループ画像: オフ"
        cl.replyMessage(msg, md)
        
    @tracer.Command(inpart=True,permissions=["Admin","White"])
    def addwhite(self,cl,msg):
        mts = self.getMention(msg.contentMetadata)
        added  = ""
        for m in mts:
            if m not in protect['whiteUsers']:
                protect['whiteUsers'][whiteUserMid] = True
                added  += cl.getContact(m).displayName + "\n"
        if added != "":
            cl.replyMessage(msg, "%s\nAdded these users to whitelist!"%(added))
        else:
            cl.replyMessage(msg, "All mentioned users are already in whitelist!")
        
    @tracer.Command(permissions=["Admin","White"])
    def 保護_オン(self,cl,msg):
        if msg.to in protect['normalProtect']:
            cl.replyMessage(msg, "保護機能はすでに有効になっています。")
        else:
            protect['normalProtect'][msg.to] = True
            readData = codecs.open('./normalProtect.json','w','utf-8')
            json.dump(protect['normalProtect'], readData, sort_keys=True, indent=4, ensure_ascii=False)
            cl.replyMessage(msg, "保護機能を有効にしました。")
        
    @tracer.Command(permissions=["Admin","White"])
    def 保護_オフ(self,cl,msg):
        if msg.to in protect['normalProtect']:
            del protect['normalProtect'][msg.to]
            readData = codecs.open('./normalProtect.json','w','utf-8')
            json.dump(protect['normalProtect'], readData, sort_keys=True, indent=4, ensure_ascii=False)
            cl.replyMessage(msg, "保護機能を解除しました。")
        else:
            cl.replyMessage(msg, "保護機能はすでに無効になっています。")

    @tracer.Command(permissions=["Admin","White"])
    def 保護_名前_オン(self,cl,msg):
        if msg.to in protect['groupName']:
            cl.replyMessage(msg, "グループ名の保護機能はすでに有効になっています。")
        else:
            protect['groupName'][msg.to] = cl.getGroup(msg.to).name
            f=codecs.open('./groupName.json','w','utf-8')
            json.dump(protect['groupName'], f, sort_keys=True, indent=4,ensure_ascii=False)
            cl.replyMessage(msg, "グループ名の保護機能を有効にしました。")
        
    @tracer.Command(permissions=["Admin","White"])
    def 保護_名前_オフ(self,cl,msg):
        if msg.to in protect['groupName']:
            del protect['groupName'][msg.to]
            readData = codecs.open('./groupName.json','w','utf-8')
            json.dump(protect['groupName'], readData, sort_keys=True, indent=4, ensure_ascii=False)
            cl.replyMessage(msg, "グループ名の保護機能を解除しました。")
        else:
            cl.replyMessage(msg, "グループ名の保護機能はすでに無効になっています。")
        
    @tracer.Command(permissions=["Admin","White"])
    def 保護_画像_オン(self,cl,msg):
        if msg.to in protect['groupPicture']:
            cl.replyMessage(msg, "グループ画像の保護機能はすでに有効になっています。")
        else:
            try:
                imageName = random_string(10) + ".png"
                download_img("http://dl.profile.line-cdn.net/"+cl.getGroup(msg.to).pictureStatus, imageName)
                protect['groupPicture'][msg.to] = imageName
                readData = codecs.open('./groupPicture.json', 'w', 'utf-8')
                json.dump(protect['groupPicture'], readData, sort_keys=True, indent=4, ensure_ascii=False)
                cl.replyMessage(msg, "グループ画像の保護機能を有効にしました。")
            except:
                cl.replyMessage(msg, "グループ画像が設定されていません。\n設定してからこのコマンドを実行してください。")
        
    @tracer.Command(permissions=["Admin","White"])
    def 保護_画像_オフ(self,cl,msg):
        if msg.to in protect['groupPicture']:
            imagePath = "./" + protect['groupPicture'][msg.to]
            os.remove(imagePath)
            del protect['groupPicture'][msg.to]
            readData = codecs.open('./groupPicture.json','w','utf-8')
            json.dump(protect['groupPicture'], readData, sort_keys=True, indent=4, ensure_ascii=False)
            cl.replyMessage(msg, "グループ画像の保護機能を解除しました。")
        else:
            cl.replyMessage(msg, "グループ名の保護機能はすでに無効になっています。")
        
    @tracer.Command(permissions=["Admin","White"])
    def 保護_url_オン(self,cl,msg):
        if msg.to in protect['groupUrl']:
            cl.replyMessage(msg, "グループurlの保護機能はすでに有効になっています。")
        else:
            protect['groupUrl'][msg.to] = True
            readData = codecs.open('./groupUrl.json', 'w', 'utf-8')
            json.dump(protect['groupUrl'], readData, sort_keys=True, indent=4, ensure_ascii=False)
            cl.replyMessage(msg, "グループurlの保護機能を有効にしました。")
            G =cl.getGroup(msg.to)
            G.preventJoinByTicket = True
            cl.updateGroup(G)
        
    @tracer.Command(permissions=["Admin","White"])
    def 保護_url_オフ(self,cl,msg):
        if msg.to in protect['groupUrl']:
            del protect['groupUrl'][msg.to]
            readData = codecs.open('./groupUrl.json','w','utf-8')
            json.dump(protect['groupUrl'], readData, sort_keys=True, indent=4, ensure_ascii=False)
            cl.replyMessage(msg, "グループurlの保護機能を解除しました。")
        else:
            cl.replyMessage(msg, "グループurlの保護機能はすでに無効になっています。")
        
    @tracer.Command(permissions=["Admin","White"])
    def 招待URL許可(self,cl,msg):
        group = client.getGroup(msg.to)
        if group.preventedJoinByTicket == False:
            cl.replyMessage(msg, "既に許可されています。")
        else:
            if msg.to in protect['groupUrl']:
                cl.replyMessage(msg, "招待URLの設定変更が禁止されているので作成できません。\n保護 URL オフを実行してください。")
            else:
                group.preventedJoinByTicket = False
                client.updateGroup(group)
                cl.replyMessage(msg, "URL招待を許可しました。")
        
    @tracer.Command(permissions=["Admin","White"])
    def 招待URL拒否(self,cl,msg):
        group = cl.getGroup(msg.to)
        if group.preventedJoinByTicket == True:
            cl.replyMessage(msg, "既に拒否されています")
        else:
            group.preventedJoinByTicket = True
            cl.updateGroup(group)
            cl.replyMessage(msg, "URL招待を拒否しました")

tracer.addClass(FuncPs())
tracer.addClass(OpPs())
tracer.addClass(CmdPs())
tracer.run()
