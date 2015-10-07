from .forms import RedPostDetailedSearchForm
from app_lod.models import GLORIOUS_SECTIONS
from app_database.datatables_ssp import DataTablesServerSideProcessor
from utilities.snippets import JSONObjectIdEncoder, to_markdown

class RedPostsSSP(DataTablesServerSideProcessor):
    def filter(self):
        # Columns specific search
        # I'm going to make something ugly there don't mind me please
        # I promise I'll clean everything when it works !!!!!!
        # TODO : Clean this so it's reusable somehow
        for c in self.columns:
            if c['search']['value'] != '':
                if c['data'] == 0:
                    # Filter for THAT Rioter
                    if 'rioter' not in self.dt_query:
                        self.dt_query['rioter'] = []
                    self.dt_query['rioter'].append(c['search']['value'])
                if c['data'] == 'region':
                    if 'region' not in self.dt_query:
                        self.dt_query['region'] = []
                    self.dt_query['region'].extend(c['search']['value'].split('|'))
                if c['data'] == 'is_glorious':
                    if c['search']['value'] == 'true':
                        if 'section' not in self.dt_query:
                            self.dt_query['section'] = []
                        self.dt_query['section'].extend(GLORIOUS_SECTIONS)
        mongo_query = RedPostDetailedSearchForm(self.dt_query).get_search()
        workon = mongo_query
        # Deconstruct the query
        if len(mongo_query.keys()) == 0:
            key = ''
        else:
            key = list(mongo_query.keys())[0]
        if key in ['$or', '$and']:
            workon = {k: v for k, v in [list(t.items())[0] for t in mongo_query[key]]}
        # Text search
        if self.dt_search is not None and self.dt_search['value'] != "":
            if '$text' in workon and '$search' in workon['$text']:
                workon['$text']['$search'] = workon['$text']['$search'] + ' ' + self.dt_search['value']
            else:
                workon['$text'] = {'$search': self.dt_search['value']}
        # Rebuild the query if necessary
        if key in ['$or', '$and']:
            workon = {key: [{k: v} for k, v in workon.items()]}
        self.query = workon

    def data_postprocess(self):
        data = list(self.result_data)
        for d in data:
            d['contents'] = to_markdown(d['contents'])
        self.result_data = data