import threading
import pika
import datetime
from send_email_overstock import send_email

##################################################
# MQ 地址
mq_ip = 'localhost'
# MQ 端口
mq_port = 5672
##################################################
# 检查频率（秒）
check_overstock_loop = 60
##################################################
# 待检查的队列列表
queue_list = ['q1','q2']
# 队列消息积压数阈值
queue_count = 100000
##################################################

try:
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()
except:
    print('RabbitMQ服务器连接失败，请检查网络。')


# 检查MQ队列积压
def check_overstock():
    global queue_list
    global queue_list_declared
    global channel
    global queue_count
    global check_overstock_timer

    print('Check OverStock Loop:', datetime.datetime.now())

    # 声明的消息队列，每次循环时清空。
    queue_list_declared = []

    for q in queue_list:
        # 需要循环声明，否则队列信息不刷新。
        queue = channel.queue_declare(queue=q, durable=True)
        queue_list_declared.append(queue)

    for q in queue_list_declared:
        q_count = q.method.message_count
        # debug
        # print(q, q_count)
        if q_count > queue_count:
            # debug
            # print('Send mark')
            send_email()
        else:
            pass
    # 因为定时器构造后只执行1次，必须循环调用。
    timer = threading.Timer(check_overstock_loop, check_overstock, args=())
    timer.start()

# 首次启动时用：
check_overstock_timer = threading.Timer(check_overstock_loop, check_overstock, args=())
check_overstock_timer.start()
