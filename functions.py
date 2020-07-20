import time

def getDate(timeStamp):
    timeArray = time.localtime(timeStamp)
    timeStyled = time.strftime("%Y-%m-%d", timeArray)
    return timeStyled

if __name__=="__main__":
    print(getDate(1563796861))