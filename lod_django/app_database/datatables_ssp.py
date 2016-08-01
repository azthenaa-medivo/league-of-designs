import itertools
import json
from app_database.consumer import MongoConsumer

# translation for sorting between datatables and mongodb
order_dict = {'asc': 1, 'desc': -1}

class DataTablesServerSideProcessor(object):
    """A basic class that handles most of whatever an SSP is supposed to handle. Subclass it.
    Expect json encapsulated in an "args" field."""
    def __init__(self, request, database, collection, fields=None):
        tmp_args = json.loads(request.GET.get('args'))
        self.consumer = MongoConsumer(database)
        self.collection = collection
        self.columns = tmp_args['columns']
        self.fields = [c["name"] for c in self.columns]
        if len(self.fields) == 0:
            self.fields = fields
        self.dt_skip = tmp_args['start']
        self.dt_length = tmp_args['length']
        self.dt_sorting = tmp_args['order']
        # Query : we have to merge Datatable's "search" and my own.
        self.dt_query = tmp_args['query'] if 'query' in tmp_args else {}
        self.dt_search = tmp_args['search']
        self.is_search = self.dt_search['value'] != '' or "search" in self.dt_query
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
                                             skip=self.dt_skip, limit=self.dt_length)
        if len(self.sorting) > 0:
            self.result_data = self.result_data.sort(self.sorting)
        self.records_filtered = self.result_data.count()
        self.records_total = self.consumer.get(self.collection).count()
        self.data_postprocess()

    def filter(self):
        """Basic filtering using the text input, override this in your subclass if you want to be more specific."""
        if self.is_search != '':
            self.query['$text'] = {'$search': self.dt_search}
            self.projection['META_score'] = {'$meta': 'textScore'}

    def sort(self):
        # Handling META_score : we sort on META_score only if there was a text search AND we want to sort by score.
        sort_score = False
        for o in self.dt_sorting:
            if self.fields[o['column']] == "META_score":
                sort_score = True
                self.fields = [f for f in self.fields if f != "META_score"]
                self.dt_sorting = [f for f in self.dt_sorting if f != o]
                break
        self.sorting = list((("META_score", {"$meta": "textScore"}) if self.is_search and sort_score
                        else (self.fields[o['column']], order_dict[o['dir']]) for o in self.dt_sorting))

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
