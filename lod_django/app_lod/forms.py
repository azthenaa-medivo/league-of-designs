import itertools
from django.forms import Form, CharField, ChoiceField, BooleanField, Textarea, HiddenInput, TextInput
from .models import STATUS, ARTICLE_TYPE
from app_database.consumer import Consumer

consumer = Consumer()

class ChampionForm(Form):
    _id = CharField(widget=HiddenInput)
    summary = CharField(widget=Textarea)
    status = ChoiceField(choices=STATUS)

    def save(self):
        return consumer.update_champion(self.cleaned_data)

    def is_valid(self):
        return super(Form, self).is_valid() and len(self.cleaned_data['_id']) == 24

class NewArticleForm(Form):
    _id = CharField(widget=HiddenInput)
    title = CharField(required=True, widget=TextInput(attrs={'size': '60'}))
    url_id = CharField(required=False, widget=TextInput(attrs={'size': '60'}))
    author = CharField()
    champion = ChoiceField(choices=itertools.chain((('None', '--- None ---'),), ((c['name'], c['name']) for c in
                                    list(consumer.get_champions(projection={'name': 1}))),))
    type = ChoiceField(choices=ARTICLE_TYPE, required=True, initial='General')
    # We'll add 'created' and 'last_edited' fields alla mano.
    contents = CharField(required=True, widget=Textarea(attrs={'cols': '120', 'rows': 20}))

    def save(self):
        return consumer.update_article(self.cleaned_data)

    def is_valid(self):
        return super().is_valid() and len(self.cleaned_data['_id']) == 24 or self.cleaned_data['_id'] == "new"

class ArticleForm(NewArticleForm):
    _id = CharField(widget=HiddenInput)

    def is_valid(self):
        return super(NewArticleForm, self).is_valid()