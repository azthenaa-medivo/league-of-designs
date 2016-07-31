import operator
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
        # Additional text search
        # In case you search in the little Datatable box during a more global search.
        if self.is_search:
            the_value = self.dt_search['value'].strip().replace(" +", " ")
            if '$text' in workon and '$search' in workon['$text']:
                # Experimental : now looks for both terms exactly.
                workon['$text']['$search'] = "\"" + workon['$text']['$search'].replace(" ", "\" \"") + "\" \"" + the_value + "\""
            else:
                workon['$text'] = {'$search': the_value}
        # Always add the score. It'll be 0 if there's no text search.
        self.projection['META_score'] = {'$meta': 'textScore'}
        # Rebuild the query if necessary
        if key in ['$or', '$and']:
            workon = {key: [{k: v} for k, v in workon.items()]}
        self.query = workon

    def data_postprocess(self):
        super(RedPostsSSP, self).data_postprocess()
        for d in self.result_data:
            d['contents'] = to_markdown(d['contents'])
