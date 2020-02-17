
class Utility() :
    def addto(self, item, _list):
        if item not in _list :
            _list.append(item)
    def removefrom(self, item, _list) :
        if item in _list:
            _list.remove(item)
