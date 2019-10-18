import attr
from pylexibank import Language, Lexeme
from pylexibank.dataset import Dataset as BaseDataset
from pylexibank.util import pb
from clldutils.path import Path


@attr.s
class DLanguage(Language):
    Location = attr.ib(default=None)
    Variety = attr.ib(default=None)
    List_ID = attr.ib(default=None)
    SubGroup = attr.ib(default=None)
    SourceType = attr.ib(default=None)
    Latitude = attr.ib(default=None)
    Longitude = attr.ib(default=None)
    Family = attr.ib(default=None)

@attr.s
class DLexeme(Lexeme):
    Stem = attr.ib(default=None)

class Dataset(BaseDataset):
    dir = Path(__file__).parent
    id = "dagloans"
    language_class = DLanguage
    lexeme_class = DLexeme

    def cmd_download(self, **kw):
        pass

    def cmd_makecldf(self, args):
        data = self.raw_dir.read_csv('DagLoans.tsv', delimiter="\t", dicts=True)
        #ds.add_sources(*self.raw.read_bib())
        args.writer.add_concepts()
        args.writer.add_languages()
        params = {c['ENGLISH']: c['ID'] for c in self.concepts}
        langs = {c['List_ID']: c['ID'] for c in self.languages}

        for line in pb(data, desc="wl-to-cldf", total=len(data)):
            row = args.writer.add_form(
                Language_ID=langs[line['List ID']],
                Parameter_ID=params[line['Concept']],
                Value=line['Word'],
                Form=line['Word'],
                Source=[],
                Stem=line['Stem']
                )
            args.writer.add_cognate(
                lexeme=row,
                Cognateset_ID=line['Set'].replace(' ', '')
                )



