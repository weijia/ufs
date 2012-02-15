import encryptedListShove
class ShoveLike(encryptedListShove.ShoveLike):
    '''
    Both key and value should be unicode
    '''
    def __getitem__(self, key):        '''        Return a string when only 1 item is in the result.        '''
        res = encryptedListShove.ShoveLike.__getitem__(self, key)        if len(res) == 1:            return res[0]
        return res
