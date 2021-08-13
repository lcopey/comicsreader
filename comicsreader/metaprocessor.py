import re
from dataclasses import dataclass
from typing import Tuple, List


# TODO Remove multiple space in meta processing
# TODO Remove Vol, Vol. at the end of the title
# TODO Numbers for multiple volumes should be close to one another
class TitleProcessor:
    """Title Processor class. Provides helper function to infer diverses metadata from typically the file name.
    Main metadatas consists of :

    * Title
    * Date
    * Volume

    This class is not intented to be used alone but as part of :class:`.MetaProcessor`

    """

    def __init__(self, ):
        self.counter = 0

    def mark(self, input: str, pattern: str):
        token = f'{{{self.counter}}}'
        result = re.sub(pattern, token, input)
        self.counter += 1
        return result

    def infer_extension(self, file: str) -> Tuple[str, str]:
        match = file[-3:]
        processed = self.mark(file, match)
        return match, processed

    def infer_date(self, file: str) -> Tuple[List[int], str]:
        pattern = '(?:19|20)[0-9]{2}'
        match = re.findall(pattern, file)
        processed = file
        for n, value in enumerate(match):
            processed = self.mark(processed, value)
            match[n] = int(value)

        return match, processed

    def infer_volumes(self, file: str) -> Tuple[List[int], str]:
        """Infer the volume number based on the file name

        Parameters
        ----------
        file: str
            file name

        Returns
        -------
        Tuple[List[int], str]
        Returns a tuple containing the volumes number as a list of integer and the processed file name.

        """
        # firts look for v01 or Vol.01...
        vol_pattern = re.compile(r"""
                                (?!{)  # ignore when starting with {
                                ((?:v|[Vv]ol[. ]{0,2}|T)[0-9]{1,3}) # Look for numbers starting with v, vol...
                                (-(?:v|[Vv]ol[. ]{0,2}|T)[0-9]{1,3})?
                                # (?!})  # ignore when finishing with }
                                """, re.VERBOSE
                                 )
        alt_pattern = re.compile(r"""
                                (?!{)  # ignore when starting with {
                                [^A-Za-z]([0-9]{1,3})  # Numbers that don't start and finish with a letter
                                (-[^A-Za-z][0-9]{1,3})?
                                (?!})  # ignore when finishing with }

                                """, re.VERBOSE
                                 )
        match = re.search(vol_pattern, file)
        if not match:
            match = re.search(alt_pattern, file)

        if match:
            groups = list(match.groups())
        else:
            return [], file

        processed = file
        volumes = []
        for n, value in enumerate(groups):
            if value:
                processed = self.mark(processed, value)
                volumes.append(int(re.sub('[. \-a-zA-Z]', '', value)))  # remove alpha characters and cast to int

        return volumes, processed

    def infer_title(self, file: str) -> Tuple[str, str]:
        title = re.split('\{[0-9]\}', file)[0]
        title = re.sub('(\(\w+\))', '', title)
        title = re.sub('[(){}]', '', title)
        title = title.strip()
        title = re.sub('[-_ .]+[a-zA-Z]?$', '', title)
        processed = self.mark(file, title)

        # sanitize
        title = re.sub('_', ' ', title)
        title = re.sub(' +', ' ', title)
        # title = title.capitalize()
        return title, processed

    def reset(self):
        self.counter = 0

    def __call__(self, file: str) -> Tuple[str, List[int], List[int], List[int], str, str]:
        self.reset()
        extension, file = self.infer_extension(file)
        date, file = self.infer_date(file)
        volumes, file = self.infer_volumes(file)
        chapters, file = self.infer_volumes(file)
        title, file = self.infer_title(file)
        return extension, date, volumes, chapters, title, file


@dataclass
class MetaProcessor:
    """Class holding meta informations of the comics.

     Metadatas are stored as attributes of the dataclass

         * :attr:`file`, ``str``
            Name of the file processed
         * :attr:`tokenized_file`: ``str``
            Name of the file processed with metadata replaced as token {number}
         * :attr:`extension`: ``str``
            Extension of the file
         * :attr:`date`: ``List[int]``
            Date inferred from the file name. It is usually guessed as 4 characters starting with 20XX or 19XX.
         * :attr:`volumes`: ``List[int]``
            Volumes of the comics inferred from the file name. It is stored as a list in case multiple
            volumes are spaned in the file.
         * :attr:`title`: ``str``
            Title of the current book.

     """
    file: str
    tokenized_file: str
    extension: str = ''
    date: List[int] = None
    volumes: List[int] = None
    chapters: List[int] = None
    title: str = ''
    process_meta = TitleProcessor()

    def as_dict(self, ):
        """Return the MetaProcessor class as a dictionary instance

        """
        return {'file': self.file,
                'tokenized_file': self.tokenized_file,
                'extension': self.extension,
                'date': self.date,
                'volumes': self.volumes,
                'chapters': self.chapters,
                'title': self.title}

    @classmethod
    def from_file(cls, filename: str):
        """
        Create MetaProcessor class from file name.

        """
        extension, date, volumes, chapters, title, tokenized_file = cls.process_meta(filename)
        return cls(file=filename, extension=extension, date=date, volumes=volumes, chapters=chapters, title=title,
                   tokenized_file=tokenized_file)
