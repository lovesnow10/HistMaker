import logging as lg


class HtbRunBase(object):
    def __init__(self, LoopData):
        self.DataToLoop = LoopData
        pass

    def LoopOver(self):
        if type(self.DataToLoop) is list or type(self.DataToLoop) is tuple:
            for i, _val in enumerate(self.DataToLoop):
                lg.logging('Start running %i in List' % (i), 'SUCCESS')
                self.Do(_val)
        elif type(self.DataToLoop) is dict:
            for _key, _val in self.DataToLoop.items():
                lg.logging('Start running %s' % (_key), 'SUCCESS')
                self.Do(_val)

    def Do(self, _in):
        '''For a base class, do nothing. Please overload'''
        pass
