import smtplib
import time
import datetime
from email.mime.text import MIMEText
##################################################
# 用户名和密码
mail_user = '***@qq.com'
mail_password = '***'
# 发信人和收信人
mail_sender = mail_user
mail_receivers = u'***@qq.com'
##################################################
# 邮件发送频率阈值（秒）
email_loop = 1800
# 默认邮件发送时间戳
time_stamp = 0
##################################################
# 标题和内容
mail_subject = '【警告】RabbitMQ消息队列可能出现积压，请尽快排查原因。'
mail_content = '''@all 请收件人注意：

以下队列可能出现消息积压，请尽快解决。

    '***', 
    '***', 

'''
##################################################
msg = MIMEText(mail_content)
msg['From'] = mail_sender
msg['To'] = mail_receivers
msg['Subject'] = mail_subject
##################################################


def send_email():
    global time_stamp
    time_stamp_now = int(time.time())
    if time_stamp_now - time_stamp > email_loop:
        try:
            s = smtplib.SMTP_SSL('smtp.qq.com', 465)
            s.login(mail_user, mail_password)
            s.sendmail(mail_sender, mail_receivers, msg.as_string())
            print('邮件（消息积压告警）发送成功：', datetime.datetime.now())
        except Exception as e:
            print(e)
        finally:
            s.quit()
        # 更新最后一次邮件发送时间戳
        time_stamp = int(time.time())
    else:
        pass
