#Holds python classes used

class TextBlock(object):
    def __init__(self, aDict=None):
        """The id pointing the book in the database(int)"""
        self.book_id = None
        """The date range(list[,])"""
        self.date_range = None
        """The first 100 words(string)"""
        self.fText = None
        """City text(string)"""
        self.cText = None
        """The last 100 words(string)"""
        self.lText = None
        """The date of the map used for the city(string)"""
        self.map_date = None

        if aDict is not None:
            for k in aDict:
                if hasattr(self, k):
                    setattr(self, k, aDict[k])


#pylint: disable=w0612,w0105,r0902
class BookMeta(object):
    """Struct to hold meta data for a Book"""
    def __init__(self, aDict=None):
        """Can input a dictionary to convert"""
        #Variables
        """The title of book(string)"""
        self.title = None
        """The writer of book(string)"""
        self.creator = None
        """Date published(string)"""        
        self.date = None
        """Publisher of book(string)"""
        self.publisher = None
        """Source of book(string)"""
        self.source = None
        """ID value for book(string)"""
        self.identifier = None
        """Type of file ie. text, image(string)"""
        self.type = None
        """Format of text ie. book, article(string)"""
        self.format = None
        """Genre of book(string)"""
        self.genre = None
        """Period/Era(string)"""
        self.period = None
        """Theme of book(string)"""
        self.theme = None
        """Gender of writer(string)"""
        self.gender = None
        """Path to text file(string)"""
        self.path = None
        """Url to book hosted(string)"""
        self.url = None
        """Number of words(int)"""
        self.words = None
        """The strength of the search. 0 = No search."""
        self.searchStrengh = 0

        if aDict is not None:
            for k in aDict:
                if hasattr(self, k):
                    setattr(self, k, aDict[k])

class Struct(object):
    def __init__(self, adict):
        """Convert a dictionary to a class

        @param :adict Dictionary
        """
        self.__dict__.update(adict)
        for k, v in adict.items():
            if isinstance(v, dict):
                self.__dict__[k] = Struct(v)

def get_object(adict):
    """Convert a dictionary to a class

    @param :adict Dictionary
    @return :class:Struct
    """
    return Struct(adict)
