import sys, datetime, time
import urllib3
# 尾递归 - Start
class TailRecurseException(BaseException):
    def __init__(self, args, kwargs):
        self.args = args
        self.kwargs = kwargs
def tail_call_optimized(g):
    def func(*args, **kwargs):
        f = sys._getframe()
        if f.f_back and f.f_back.f_back and f.f_back.f_back.f_code == f.f_code:
            raise TailRecurseException(args, kwargs)
        else:
            while 1:
                try:
                    return g(*args, **kwargs)
                except TailRecurseException as e:
                    args = e.args
                    kwargs = e.kwargs
    func.__doc__ = g.__doc__
    return func
# 尾递归 - End
# 获取当前时间
def getTime():
    commentTime = datetime.datetime.now().strftime('%m-%d %H:%M:%S')
    return commentTime
# 格式化秒数为时分秒格式
def formatSeconds(value, noBu0=0, zi=0):
    second = int(value); # 秒
    minute = 0; # 分
    hour = 0; # 小时
    if second > 60: # 秒大于60转为分钟
        minute = int(second/60);
        second = int(second%60);
        if minute > 60: # 分大于60转为小时
            hour = int(minute/60);
            minute = int(minute%60);
    def bu0(i, dw): #不足10的补0
        rs = '';
        if noBu0: #不补零
            rs = str(i);
        elif i < 10:
            rs = '0' + str(i);
        else:
            rs = str(i);
        if zi:
            return rs + dw;
        else:
            if dw == '秒':
                return rs;
            else:
                return rs + ":";
    result = bu0(second, '秒');
    if minute > 0:
        result = bu0(minute, '分') + result;
    if hour > 0:
        result = bu0(hour, '时') + result;
    return result;
# 获取两个时间戳的时间间隔
def getTimeSpace(m, n):
    second = int(n - m)
    return formatSeconds(second, 1, 1)
flag = -1; #1正常 0异常
preTime = 0; #记录上次网络正常或异常的时间
def connectNet():
    global flag, preTime;
    try:
        http = urllib3.PoolManager(retries=3, timeout=5, num_pools=200, maxsize=200)
        res = http.request('GET', 'https://www.baidu.com');
        # print(res.data)
        # print('✔网络正常 ' + getTime())
        if flag == -1:
            print('√联网正常，持续监测中... ' + getTime())
            preTime = datetime.datetime.now().timestamp();
        elif flag == 0:
            space = getTimeSpace(preTime, datetime.datetime.now().timestamp())
            print('--网络恢复：' + getTime() + '，本次断网时长：' + space + '，继续监测...')
            preTime = datetime.datetime.now().timestamp();
        flag = 1;
        return True
    except:
        if flag == -1:
            print('**已断网：' + getTime() + " 等待恢复...")
            preTime = datetime.datetime.now().timestamp();
        if flag == 1:
            space = getTimeSpace(preTime, datetime.datetime.now().timestamp())
            print('**已断网：' + getTime() + '，本次联网时长：' + space + '，等待恢复...')
            preTime = datetime.datetime.now().timestamp();
        flag = 0;
        return False
print("监测网络连接状态 By 52pojie - 云烟成雨")
print("-"*45)
# 递归调用
@tail_call_optimized
def loopRun():
    connectNet();
    time.sleep(1)
    loopRun()
loopRun()
