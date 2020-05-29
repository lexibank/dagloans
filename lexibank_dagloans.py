import attr
from pylexibank import Language, Lexeme, Concept
from pylexibank.dataset import Dataset as BaseDataset
from pylexibank.util import progressbar
from clldutils.path import Path
from clldutils.misc import slug


@attr.s
class CustomLanguage(Language):
    Location = attr.ib(default=None)
    Variety = attr.ib(default=None)
    List_ID = attr.ib(default=None)
    SubGroup = attr.ib(default=None)
    SourceType = attr.ib(default=None)
    Latitude = attr.ib(default=None)
    Longitude = attr.ib(default=None)
    Family = attr.ib(default=None)
    District = attr.ib(default=None)
    Source = attr.ib(default=None)
    SfW = attr.ib(default=None)
    

@attr.s
class CustomConcept(Concept):
    Number = attr.ib(default=None)


@attr.s
class CustomLexeme(Lexeme):
    Stem = attr.ib(default=None)
    Lexeme_ID = attr.ib(default=None)


class Dataset(BaseDataset):
    dir = Path(__file__).parent
    id = "dagloans"
    language_class = CustomLanguage
    lexeme_class = CustomLexeme
    concept_class = CustomConcept

    def cmd_makecldf(self, args):
        data = self.raw_dir.read_csv('DagLoans_Words.tsv', delimiter="\t", dicts=True)
        args.writer.add_sources()
        concepts = {}
        for concept in self.concepts:
            idx = '{0}_{1}'.format(concept['NUMBER'], slug(concept['ENGLISH']))
            args.writer.add_concept(
                    ID=idx,
                    Name=concept['ENGLISH'],
                    Number=concept['NUMBER'])
            concepts[concept['ENGLISH']] = idx
        sources, languages = {}, {}
        for language in self.languages:
            if language['District'] == 'Dictionary':
                sources[language['List_ID']] = language['Source'].strip()
                language['District'] = ''
            elif language['District'] == 'Expert':
                language['District'] = ''
            args.writer.add_language(**language)
            languages[language['List_ID']] = language['ID']

        for row in progressbar(data):
            lexeme = args.writer.add_form(
                Language_ID=languages[row['List_ID']],
                Parameter_ID=concepts[row['Concept']],
                Local_ID=row['Entry_ID'],
                Value=row['Standard_Transcription'],
                Form=row['Word'],
                Source=sources.get(row['List_ID'], ''),
                Stem=row['Stem']
                )
            #args.writer.add_cognate(
            #    lexeme=row,
            #    Cognateset_ID=line['Set'].replace(' ', '')
            #    )



