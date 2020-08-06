from twisted.internet import task, reactor

timeout = 600.0


def looping(f):
    loop = task.LoopingCall(f)
    loop.start(timeout)
    reactor.run()
