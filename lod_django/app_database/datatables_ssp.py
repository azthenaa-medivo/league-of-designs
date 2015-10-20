import itertools
import json
from app_database.consumer import MongoConsumer

# translation for sorting between datatables and mongodb
order_dict = {'asc': 1, 'desc': -1}

class DataTablesServerSideProcessor(object):
    """A basic class that handles most of whatever an SSP is supposed to handle. Subclass it.
    Expect json encapsulated in an "args" field."""
    def __init__(self, request, database, collection, fields):
        tmp_args = json.loads(request.GET.get('args'))
        self.consumer = MongoConsumer(database)
        self.fields = fields
        self.collection = collection
        self.columns = tmp_args['columns']
        self.dt_skip = tmp_args['start']
        self.dt_length = tmp_args['length']
        self.dt_search = tmp_args['search']
        self.is_search = self.dt_search['value'] != ''
        self.dt_sorting = tmp_args['order']
        self.dt_query = tmp_args['query'] if 'query' in tmp_args else {}
        self.dt_projection = tmp_args['projection'] if 'projection' in tmp_args else {}
        # Returned values
        self.draw = tmp_args['draw']
        self.query = {}
        self.projection = {}
        self.sorting = {}
        self.records_filtered = 0
        self.records_total = 0
        self.result_data = None
        self.run_queries()

    def run_queries(self):
        if self.dt_query is not None:
            self.filter()
        self.sort()
        self.result_data = self.consumer.get(self.collection, query=self.query, projection=self.projection if self.projection != {} else None,
                                             skip=self.dt_skip, limit=self.dt_length).sort(list(self.sorting))
        self.records_filtered = self.result_data.count()
        self.records_total = self.consumer.get(self.collection).count()
        self.data_postprocess()

    def filter(self):
        """Basic filtering using the text input, override this in your subclass if you want to be more specific."""
        if self.is_search != '':
            self.query['$text'] = {'$search': self.dt_search}
            self.projection['META_score'] = {'$meta': 'textScore'}

    def sort(self):
        self.sorting = ((self.fields[o['column']], order_dict[o['dir']]) for o in self.dt_sorting)

    def data_postprocess(self):
        """Whatever to do with self.result_data if needed."""
        self.result_data = list(self.result_data)

    def output_result(self):
        output = {
                    'draw': self.draw,
                    'recordsTotal': self.records_total,
                    'recordsFiltered': self.records_filtered,
                    'data': list(self.result_data) if self.result_data is not None else [],
                  }
        return output
