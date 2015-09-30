import datetime
from django.forms import Form, BooleanField

class MongoSearchForm(Form):
    is_and = BooleanField(required=False, initial=True, label="Match all ?",
                          help_text="""If checked (true), will try to match ALL conditions. Else, will search for every
                                    condition individually. If unchecked, additional search strings will not be
                                    processed.""")

    def get_search(self):
        if self.is_valid():
            query = {}
            is_and = True
            for field, value in self.cleaned_data.items():
                if isinstance(value, list):
                    if value:
                        query[field] = {'$in': value}
                elif isinstance(value, datetime.datetime):
                    if value:
                        field_name = '_'.join(field.split('_')[:-1])
                        if field.endswith('before'):
                            q = '$lte'
                        elif field.endswith('after'):
                            q = '$gte'
                        else:
                            query[field_name] = value
                        if field_name not in query:
                            query[field_name] = {}
                        query[field_name][q] = value
                elif field == 'search':
                    if value != '':
                        query['$text'] = {'$search': value}
                elif field == 'is_and':
                    is_and = value
            if is_and:
                op = '$and'
            else:
                op = '$or'
                if '$text' in query:
                    del query['$text']
            if len(query) > 1:
                query = {op: [{k: v} for k, v in query.items()]}
            return query
        return None