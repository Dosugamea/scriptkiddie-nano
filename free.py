# coding:utf-8
from LineApi import *
from LineApi import HooksTracer
import random, requests, shutil, codecs, json, random, os

with open("Tokens.json","r") as f:
    tokens = json.loads(f.read())
    
yukino_1 = LINE(tokens["Main"],type="IOSIPAD")
yukino_2 = LINE(tokens["Sub1"],type="IOSIPAD")
yukino_3 = LINE(tokens["Sub2"],type="IOSIPAD")

'''
with open("Help.txt","r",encoding="utf8") as f:
    helpText = f.read()
'''
helptext = [
    "--このbotのヘルプ--",
    "/mid",
    "  midを送信します",
    "/gid",
    "  gidを送信します",
    "/グル情報",
    "  グループ情報を表示します",
    "/保護 オン",
    "  保護機能を有効にします",
    "/保護 オフ",
    "  保護機能を無効にします"
]
helpText = "\n".join(helpText)          
db                 = sqlite3.connect("free_protect.db", check_same_thread=False)
tracer             = HooksTracer(yukino_1,prefix=["／","/","!","?",".","#"],db=db)
tracer.bots        = [yukino_1, yukino_2, yukino_3]
tracer.kickers     = [yukino_2, yukino_3]
tracer.botMids     = [b.getProfile().mid for b in tracer.bots]
tracer.kickerMids  = [k.getProfile().mid for k in tracer.kickers]
tracer.helptext    = helpText
profile = yukino_1.getProfile()

class OpPs(object):
    @tracer.Operation(26)
    def OPERATION_MESSAGE(self,cl,op):
        msg = op.message
        self.trace(msg,"Content")

    @tracer.Content(0)
    def CONTENT_MESSAGE(self,cl,msg):
        self.log("[MESSAGE] "+msg.text)
        self.trace(msg,"Command")

    @tracer.Operation(11)
    def NOTIFIED_UPDATE_GROUP(self,cl,op):
        self.log("NOTIFIED_UPDATE_GROUP")
        gid = op.param1
        usr = op.param2
        ctp = op.param3
        if usr != self.getGroup(gid,"Admin"):
            #Name
            if ctp == 1:
                gr = cl.getGroup(gid)
                grName = self.getGroup(gid,"OldName")
            #Picture
            elif ctp == 2:
                pass
            #UrlPrevent
            elif ctp == 4:
                pass

    @tracer.Operation(13)
    def NOTIFIED_INVITE_INTO_GROUP(self,cl,op):
        self.log("NOTIFIED_INVITE_INTO_GROUP")
        gid        = op.param1
        inviter    = op.param2
        got_inv    = op.param3
        if inviter not in self.getPermissionByName("Black"):
            cl.acceptGroupInvitation(gid)
            self.postGroup(gid,"Admin",inviter)
            cl.sendMessage(gid,"招待ありがとうございます!\n私は単独保護Botです!\nヘルプの確認には\n「!help」\nと言ってください♪")
            #リスト化するとDBにぶち込むのが非常にめんどくさいのでとりあえず招待者のみをサポートする
        
    @tracer.Operation(15)
    def NOTIFIED_LEAVE_GROUP(self,cl,op):
        self.log("NOTIFIED_LEAVE_GROUP")
        gid = op.param1
        usr = op.param2
        if usr == self.getGroup(gid,"Admin"):
            cl.leaveGroup(gid)
            
    @tracer.Operation(19)
    def NOTIFIED_KICKOUT_FROM_GROUP(self,cl,op):
        self.log("NOTIFIED_KICKOUT_FROM_GROUP")
        gid    = op.param1
        kicker = op.param2
        gotban = op.param3
        if kicker != self.getGroup(gid,"Admin"):
            cl.kickoutFromGroup(gid,kicker)
            cl.inviteIntoGroup(gid,[gotban])

class CmdPs(object):
    @tracer.Command(alt=["ヘルプ"])
    def help(self,cl,msg):
        cl.replyMessage(msg,self.helpText)

    @tracer.Command()
    def mid(self,cl,msg):
        cl.replyMessage(msg,msg._from)
        
    @tracer.Command(sources=["Group"])
    def gid(self,cl,msg):
        cl.replyMessage(msg,msg.to)
        
    @tracer.Command(sources=["Group"])
    def グル情報(self,cl,msg):
        gr = cl.getGroup(msg.to)
        cl.replyMessage(msg,str(gr))
        
    @tracer.Command(sources=["Group"])
    def 保護(self,cl,msg):
        if self.getGroup(msg.to,"Protect"):
            cl.replyMessage(msg,"現在このグループは保護有効状態です")
        else:
            cl.replyMessage(msg,"現在このグループは保護無効状態です")
        
    @tracer.Command(alt=["保護 有効"],sources=["Group"])
    def 保護_オン(self,cl,msg):
        if msg._from == self.getGroup("Admin"):
            if not self.getGroup(msg.to,"Protect"):
                self.postGroup(msg.to,"Protect",1)
                cl.replyMessage(msg,"保護状態を有効に切り替えました")
            else:
                cl.replyMessage(msg,"保護は既に有効になっています")
        else:
            cl.replyMessage(msg,"その設定はBotの招待者のみが変更できます")
        
    @tracer.Command(alt=["保護 無効"],sources=["Group"])
    def 保護_オフ(self,cl,msg):
        if msg._from == self.getGroup("Admin"):
            if self.getGroup(msg.to,"Protect"):
                self.postGroup(msg.to,"Protect",0)
                cl.replyMessage(msg,"保護状態を無効に切り替えました")
            else:
                cl.replyMessage(msg,"保護は既に無効になっています")
        else:
            cl.replyMessage(msg,"その設定はBotの招待者のみが変更できます")

tracer.addClass(OpPs())
tracer.addClass(CmdPs())
tracer.run()
