# coding:utf-8
from LineApi import *
from LineApi.hooks import HooksTracer
from collections    import OrderedDict
import random, requests, json, random, sqlite3, sys

with open("Tokens.json","r",encoding="utf8") as f:
    tokens = json.loads(f.read(),object_pairs_hook=OrderedDict)
    
with open("Help.txt","r",encoding="utf8") as f:
    helpText = f.read()

with open("authToken.txt","r") as f:
    yukino_1 = LINE(f.read(),type="IOSIPAD")
    
yukino_2 = yukino_3 = yukino_4 = yukino_5 = yukino_1

'''
yukino_2 = LINE(tokens["Sub1"],type="IOSIPAD")
yukino_3 = LINE(tokens["Sub2"],type="IOSIPAD")
yukino_4 = LINE(tokens["Sub3"],type="IOSIPAD")
yukino_5 = LINE(tokens["Sub4"],type="IOSIPAD")
'''

db                 = sqlite3.connect("protect.db", check_same_thread=False)
tracer             = HooksTracer(yukino_1,prefix=["/","!","?","."],db=db)
#tracer.generate_db()
tracer.bots        = [yukino_1, yukino_2, yukino_3, yukino_4, yukino_5]
tracer.kickers     = [yukino_2, yukino_3, yukino_4, yukino_5]
tracer.botMids     = [b.getProfile().mid for b in tracer.bots]
tracer.kickerMids  = [k.getProfile().mid for k in tracer.kickers]
tracer.helptext    = helpText

class OpPs(object):
    @tracer.Operation(26)
    def OPERATION_MESSAGE(self,cl,op):
        msg = op.message
        self.trace(msg,"Content")
    @tracer.Content(0)
    def CONTENT_MESSAGE(self,cl,msg):
        self.trace(msg,"Command")
        
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
                    pass
                    #追い出されたのがBotならリストからそれを抜く
                    #追い出したキッカーを追い出す
                    #追い出された人を再招待
                    #ブラックリストに入ってなければ登録
                #ホワイトリストユーザーがキッカー/メイン垢を追い出してしまったなら
                if kicker in whiteUsers and gotban in botMids:
                    pass
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
            if self.cl.mid in got_inv:
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
    def mid(self,cl,msg):
        cl.replyMessage(msg,msg._from)
        
    @tracer.Command(sources=["Group"])
    def gid(self,cl,msg):
        cl.replyMessage(msg,msg.to)
        
    @tracer.Command(sources=["Group"],permissions=["Admin","White"])
    def さよなら(self,cl,msg):
        cl.replyMessage(msg,"さよなら :/")
        for b in self.bots:
            b.leaveGroup(msg.to)
    
    @tracer.Command(ignoreCase=True,alt=["help","?","へるぷ"])
    def ヘルプ(self,cl,msg):
        cl.replyMessage(msg, self.helptext)
        
    @tracer.Command()
    def 権限(self,cl,msg):
        cl.replyMessage(msg, "あなたは以下の権限を持っています\n"+("\n".join(self.getPermissionById(msg._from))))
        
    @tracer.Command(sources=["Group"])
    def グル情報(self,cl,msg):
        group = cl.getGroup(msg.to)
        md =  "[グループ名]:\n"+group.name+"\n\n"
        md += "[gid]:\n"+group.id+"\n\n"
        md += "[アイコン画像]:\n"+"http://dl.profile.line-cdn.net/"
        md += group.pictureStatus+"\n"
        if group.preventedJoinByTicket:
            md += "招待URL: 拒否\n"
        else:
            md += "招待URL: 許可\n"
        md += "メンバー数: " + str(len(group.members)) + "人\n"
        if group.invitee is None:
            md += "招待中: 0人\n"
        else:
            md += "招待中: " + str(len(group.invitee)) + "人\n"
        if self.getGroup(msg.to,"normalProtect"):
            md += "保護: オン\n"
        else:
            md += "保護: オフ\n"
        if self.getGroup(msg.to,"protectGroupUrl"):
            md += "保護 URL: オン\n"
        else:
            md += "保護 URL: オフ\n"
        if self.getGroup(msg.to,"protectGroupName"):
            md += "保護 グループ名: オン\n"
        else:
            md += "保護 グループ名: オフ\n"
        if self.getGroup(msg.to,"protectGroupPicture"):
            md += "保護 グループ画像: オン\n"
        else:
            md += "保護 グループ画像: オフ\n"
        cl.replyMessage(msg, md)
        
    @tracer.Command(sources=["Group"],inpart=True,permissions=["Admin","White"])
    def ホワリス追加(self,cl,msg):
        mts = self.getMention(msg.contentMetadata)
        added  = ""
        for m in mts:
            if "White" not in cl.getPermissionById(m):
                self.addPermission(m,"White")
                added  += cl.getContact(m).displayName + "\n"
        if added != "":
            cl.replyMessage(msg, "%s\nこれらのユーザーをホワイトリストに追加しました"%(added))
        else:
            cl.replyMessage(msg, "メンションされたユーザーは既にホワイトリストに入っています")
            
    @tracer.Command(sources=["Group"],inpart=True,permissions=["Admin"])
    def ホワリス削除(self,cl,msg):
        mts = self.getMention(msg.contentMetadata)
        removed  = ""
        for m in mts:
            if "White" in cl.getPermissionById(m):
                self.removePermission(m,"White")
                removed  += cl.getContact(m).displayName + "\n"
        if removed != "":
            cl.replyMessage(msg, "%s\nこれらのユーザーをホワイトリストから削除しました"%(removed))
        else:
            cl.replyMessage(msg, "メンションされたユーザーは既にホワイトリストに入っていません")
        
    @tracer.Command(sources=["Group"],permissions=["Admin","White"])
    def 保護オン(self,cl,msg):
        if not self.getGroup(msg.to,"normalProtect"):
            self.postGroup(msg.to,'normalProtect',True)
            cl.replyMessage(msg, "保護機能を有効にしました。")
        else:
            cl.replyMessage(msg, "保護機能はすでに有効になっています。")
        
    @tracer.Command(sources=["Group"],permissions=["Admin","White"])
    def 保護オフ(self,cl,msg):
        if self.getGroup(msg.to,"normalProtect"):
            self.postGroup(msg.to,'normalProtect',False)
            cl.replyMessage(msg, "保護機能を解除しました。")
        else:
            cl.replyMessage(msg, "保護機能はすでに無効になっています。")
            
    @tracer.Command(sources=["Group"],permissions=["Admin","White"])
    def 保護名前オン(self,cl,msg):
        if not self.getGroup(msg.to,"protectGroupName"):
            self.postGroup(msg.to,'protectGroupName',True)
            self.postGroup(msg.to,'groupName',cl.getGroup(msg.to).name)
            cl.replyMessage(msg, "グループ名の保護機能を有効にしました。")
        else:
            cl.replyMessage(msg, "グループ名の保護機能はすでに有効になっています。")
            
    @tracer.Command(sources=["Group"],permissions=["Admin","White"])
    def 保護名前オフ(self,cl,msg):
        if self.getGroup(msg.to,"protectGroupName"):
            self.postGroup(msg.to,'protectGroupName',False)
            cl.replyMessage(msg, "グループ名の保護機能を解除しました。")
        else:
            cl.replyMessage(msg, "グループ名の保護機能はすでに無効になっています。")
        
    @tracer.Command(sources=["Group"],permissions=["Admin","White"])
    def 保護画像オン(self,cl,msg):
        if not self.getGroup(msg.to,"protectGroupImage"):
            gp = cl.getGroup(msg.to).pictureStatus
            resp = requests.get("http://dl.profile.line-cdn.net/"+gp)
            with open(msg.to+".jpg","wb") as f:
                f.write(resp.content)
            self.postGroup(msg.to,"protectGroupImage",True)
            cl.replyMessage(msg, "グループ画像の保護機能を有効にしました。")
        else:
            cl.replyMessage(msg, "グループ画像の保護機能はすでに有効になっています。")
        
    @tracer.Command(sources=["Group"],permissions=["Admin","White"])
    def 保護画像オフ(self,cl,msg):
        if self.getGroup(msg.to,"protectGroupImage"):
            self.postGroup(msg.to,"protectGroupImage",False)
            cl.replyMessage(msg, "グループ画像の保護機能を解除しました。")
        else:
            cl.replyMessage(msg, "グループ画像の保護機能はすでに無効になっています。")
            
    @tracer.Command(alt=["保護うあるオン"],ignoreCase=True,sources=["Group"],permissions=["Admin","White"])
    def 保護URLオン(self,cl,msg):
        if not self.getGroup(msg.to,"protectGroupUrl"):
            self.postGroup(msg.to,'protectGroupUrl',True)
            cl.replyMessage(msg, "保護機能を有効にしました。")
        else:
            cl.replyMessage(msg, "保護機能はすでに有効になっています。")
        
    @tracer.Command(alt=["保護うあるオフ"],ignoreCase=True,sources=["Group"],permissions=["Admin","White"])
    def 保護URLオフ(self,cl,msg):
        if self.getGroup(msg.to,"protectGroupUrl"):
            self.postGroup(msg.to,'protectGroupUrl',False)
            cl.replyMessage(msg, "グループurlの保護機能を無効にしました。")
        else:
            cl.replyMessage(msg, "グループurlの保護機能はすでに無効になっています。")
        
    @tracer.Command(alt=["招待うある許可"],ignoreCase=True,sources=["Group"],permissions=["Admin","White"])
    def 招待URL許可(self,cl,msg):
        gr = cl.getGroup(msg.to)
        if gr.preventedJoinByTicket:
            gr.preventedJoinByTicket = False
            cl.updateGroup(gr)
            cl.replyMessage(msg, "招待URLからの参加を許可にしました。")
        else:
            cl.replyMessage(msg, "既に許可されています。")

    @tracer.Command(alt=["招待うある拒否"],ignoreCase=True,sources=["Group"],permissions=["Admin","White"])
    def 招待URL拒否(self,cl,msg):
        gr = cl.getGroup(msg.to)
        if not gr.preventedJoinByTicket:
            gr.preventedJoinByTicket = Trues
            cl.updateGroup(gr)
            cl.replyMessage(msg, "招待URLからの参加を拒否にしました。")
        else:
            cl.replyMessage(msg, "既に拒否されています。")
            
class AdminCmdPs(object):
    @tracer.Command(permissions=["Admin"],alt=["exec"],inpart=True)
    def execute_message(self,cl,msg):
        '''Execute Message as Python Script'''
        with open("temp.txt","w") as t:
            sys.stdout = t
            try:
                exec(msg.text.replace(self.getPrefix(msg.text)+"exec",""))
            except:
                print(traceback.format_exc())
        sys.stdout = sys.__stdout__
        with open("temp.txt","r") as r:
            cl.replyMessage(msg,r.read())

    @tracer.Command(inpart=True,permissions=["Admin"])
    def givePermission(self,cl,msg):
        users = self.getMention(msg.contentMetadata)
        args  = self.getArg(["givepermission"],msg.text,True)
        if users == []:
            self.cl.replyMessage(msg,"You must mention users to give.")
            return
        if args == []:
            self.cl.replyMessage(msg,"You must specify permissions to give.")
            return
        arg = args[0]
        users = list(set(users))
        for u in users:
            self.addPermission(u,[arg])
        usrt = "\n".join([cl.getContact(u).displayName for u in users])
        self.cl.replyMessage(msg,"Gave permission 「%s」 to below users.\n\n%s"%(arg,usrt))
        
    @tracer.Command(inpart=True,permissions=["Admin"])
    def takePermission(self,cl,msg):
        users = self.getMention(msg.contentMetadata)
        args  = self.getArg(["takepermission"],msg.text,True)
        if users == []:
            self.cl.replyMessage(msg,"You must mention users to give.")
            return
        if args == []:
            self.cl.replyMessage(msg,"You must specify permissions to give.")
            return
        arg = args[0]
        users = list(set(users))
        for u in users:
            self.removePermission(u,[arg])
        usrt = "\n".join([cl.getContact(u).displayName for u in users])
        self.cl.replyMessage(msg,"Removed permission 「%s」 from below users.\n\n%s"%(arg,usrt))

tracer.addClass(OpPs())
tracer.addClass(CmdPs())
tracer.addClass(AdminCmdPs())
tracer.run()