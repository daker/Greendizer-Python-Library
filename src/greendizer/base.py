import re
from math import modf
from datetime import datetime, timedelta




## {{{ http://code.activestate.com/recipes/65215/ (r5)
EMAIL_PATTERN = re.compile('^.+\\@(\\[?)[a-zA-Z0-9\\-\\.]' \
                           '+\\.([a-zA-Z]{2,3}|[0-9]{1,3})(\\]?)$')




def to_unicode(text):
    '''
    Converts an input text to a unicode object.
    @param text:object Input text
    @returns:unicode
    '''
    return text.decode("UTF-8") if type(text) == str else unicode(text)




def to_byte_string(text):
    '''
    Converts an input text to a unicode object.
    @param text:object Input text
    @returns:unicode
    '''
    return text.encode("UTF-8") if type(text) == unicode else str(text)




def is_valid_email(s):
    '''
    Returns a value indicating whether the submitted string is a valid
    email address.
    @param s:str Email
    @return: bool
    '''
    return (s and len(s) > 7 and EMAIL_PATTERN.match(s))




def timestamp_to_datetime(s):
    '''
    Parses a timestamp to a datetime instance.
    @param: s:str Timestamp string.
    @return: datetime
    '''
    f, i = modf(long(s) / float(1000))
    return datetime.fromtimestamp(i) + timedelta(milliseconds=f * 1000)




def datetime_to_timestamp(d):
    '''
    Converts a datetime instance into a timestamp string.
    @param d:datetime Date instance
    @return:long
    '''
    return long(d.strftime("%s") + "%03d" % (d.time().microsecond / 1000))




def extract_id_from_uri(s):
    '''
    Returns the ID section of an URI.
    @param s:str URI
    @return: str
    '''
    return [ item for item in s.split("/") if item ][-1]




class Address(object):
    '''
    Represents a postal address.
    '''
    def __init__(self, address_dict={}, mutable=False):
        '''
        Initializes a new instance of the Address class.
        @param address_dict:dict Address dictionary.
        '''
        self.__address_dict = address_dict
        self.__mutable = mutable


    def __getattr__(self, field):
        '''
        Gets a field of the address.
        @param field:str Field name.
        @return: str
        '''
        try:
            return self.__address_dict[field]
        except KeyError:
            raise AttributeError, field


    def __setattribute__(self, field, value):
        '''
        Sets an address field.
        @param field:str Field name.
        @param value:str Field value.
        '''
        if not self.__mutable:
            raise Exception("Address is not mutable.")

        if field not in ["number", "street", "city", "zipcode", "state",
                         "country"]:
            raise AttributeError("Address has no such attribute.")

        self.__address_dict[field] = value

