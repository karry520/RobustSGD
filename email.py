# -*- coding: utf-8 -*-


import smtplib
from email.header import Header
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage


def sendMail():
    # 定义相关数据,请更换自己的真实数据
    smtpserver = 'smtp.163.com'
    sender = '18216028246@163.com'
    # receiver可设置多个，使用“,”分隔
    receiver = '884816926@qq.com'
    username = '18216028246@163.com'
    password = '654123GOOD?'

    msg = MIMEMultipart()
    boby = """
    <h3>Hi，Kaiyun</h3>
    <p>实验结果已经出来啦！</p>
    """
    mail_body = MIMEText(boby, _subtype='html', _charset='utf-8')
    msg['Subject'] = Header("实验结果报告", 'utf-8')
    msg['From'] = sender
    receivers = receiver
    toclause = receivers.split(',')
    msg['To'] = ",".join(toclause)
    print(msg['To'])
    msg.attach(mail_body)

    with open("Eva/1.jpg", "rb") as f:
        images = MIMEImage(f.read())

    images.add_header('Content-ID', '<image1>')
    msg.attach(images)

    try:
        smtp = smtplib.SMTP()
        smtp.connect(smtpserver)
        smtp.login(username, password)
        smtp.sendmail(sender, toclause, msg.as_string())
    except:
        print("邮件发送失败！！")
    else:
        print("邮件发送成功")
    finally:
        smtp.quit()


sendMail()

# msg = MIMEMultipart()
#
# boby = """
#     <h3>Hi，all</h3>
#     <p>附件为本次FM_自动化测试报告。</p>
#     <p>请解压zip，并使用Firefox打开index.html查看本次自动化测试报告结果。</p>
#     <p>
#     <br><img src="cid:image1"></br>
#     </p>
#     <p>
# """


# msg.attach(mail_body)
# fp = open("/image/1.png", 'rb')
# images = MIMEImage(fp.read())
# fp.close()
# images.add_header('Content-ID', '<image1>')
# msg.attach(images)
