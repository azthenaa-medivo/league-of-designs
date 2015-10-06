import json
from .forms import RedPostDetailedSearchForm
from app_lod.models import GLORIOUS_SECTIONS
from app_database.consumer import MongoConsumer
from django.http import HttpResponse
from utilities.snippets import JSONObjectIdEncoder, to_markdown

# translation for sorting between datatables and mongodb
order_dict = {'asc': 1, 'desc': -1}

class DataTablesRedPostsServer(object):
    def __init__(self, request, collection, fields):
        tmp_args = json.loads(request.GET.get('args'))
        self.fields = fields
        self.collection = collection
        self.columns = tmp_args['columns']
        self.dt_skip = tmp_args['start']
        self.dt_length = tmp_args['length']
        self.dt_search = tmp_args['search']
        self.dt_sorting = tmp_args['order']
        self.dt_query = tmp_args['query'] if 'query' in tmp_args else {}
        self.consumer = MongoConsumer('lod')
        # Returned values
        self.draw = tmp_args['draw']
        self.query = {}
        self.sorting = {}
        self.records_filtered = 0
        self.records_total = 0
        self.result_data = None
        self.run_queries()

    def run_queries(self):
        if self.dt_query is not None:
            self.filter()
        self.sort()
        self.result_data = self.consumer.get(self.collection, query=self.query, skip=self.dt_skip,
                                                       limit=self.dt_length).sort(self.sorting)
        self.records_filtered = self.result_data.count()
        self.records_total = self.consumer.get(self.collection).count()
        # We really need to make it more cool
        data = list(self.result_data)
        for d in data:
            d['contents'] = to_markdown(d['contents'])
        self.result_data = data
        # End of ugliness

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

    def sort(self):
        self.sorting = list((self.fields[o['column']], order_dict[o['dir']]) for o in self.dt_sorting)

    def output_result(self):
        output = {
                    'draw': self.draw,
                    'recordsTotal': self.records_total,
                    'recordsFiltered': self.records_filtered,
                    'data': list(self.result_data) if self.result_data is not None else [],
                  }
        return output
