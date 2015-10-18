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
        self.project()
        self.result_data = self.consumer.get(self.collection, query=self.query, skip=self.dt_skip,
                                                       limit=self.dt_length).sort(self.sorting)
        self.records_filtered = self.result_data.count()
        self.records_total = self.consumer.get(self.collection).count()
        self.data_postprocess()

    def filter(self):
        """Basic filtering using the text input, override this in your subclass if you want to be more specific."""
        if self.dt_search != '':
            self.query['$text'] = {'$search': self.dt_search}

    def project(self):
        for p in self.dt_projection:
            self.projection[p] = 1

    def sort(self):
        self.sorting = list((self.fields[o['column']], order_dict[o['dir']]) for o in self.dt_sorting)

    def data_postprocess(self):
        """Whatever to do with the data if needed."""
        pass

    def output_result(self):
        output = {
                    'draw': self.draw,
                    'recordsTotal': self.records_total,
                    'recordsFiltered': self.records_filtered,
                    'data': list(self.result_data) if self.result_data is not None else [],
                  }
        return output