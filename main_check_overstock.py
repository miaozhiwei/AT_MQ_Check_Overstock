import threading
import pika
import datetime
from send_email_overstock import send_email

##################################################
# MQ 地址
mq_ip = 'localhost'
# MQ 端口
mq_port = 15671
##################################################
# 检查频率（秒）
check_overstock_loop = 60
##################################################
# 待检查的队列列表
queue_list = ['***', '***']
# 队列消息积压数阈值
queue_count = 100000
##################################################
# 声明的消息队列，不用关注。
queue_list_declared = []
##################################################
try:
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()
    for q in queue_list:
        queue = channel.queue_declare(queue=q, durable=True)
        queue_list_declared.append(queue)
except:
    print('RabbitMQ服务器连接失败，请检查网络。')


# 检查MQ队列积压
def check_overstock():
    global queue_count
    print('Check Loop:', datetime.datetime.now())
    for q in queue_list_declared:
        q_count = q.method.message_count
        if q_count > queue_count:
            send_email()
        else:
            pass
    # 因为定时器构造后只执行1次，必须循环调用。
    global check_overstock_timer
    timer = threading.Timer(check_overstock_loop, check_overstock, args=())
    timer.start()

# 首次启动时用：
check_overstock_timer = threading.Timer(check_overstock_loop, check_overstock, args=())
check_overstock_timer.start()
