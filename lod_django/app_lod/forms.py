import datetime
import itertools
import string
from django.forms import Form, CharField, ChoiceField, MultipleChoiceField, Textarea, HiddenInput, TextInput, \
                            DateTimeField, DateInput, BooleanField, CheckboxSelectMultiple, SelectMultiple
from .models import STATUS, ARTICLE_TYPE, TAGS, ROLES, ALL_SECTIONS, REGIONS, DATE_FORMATS
from app_database.consumer import Consumer
from utilities.mixins import MongoSearchForm

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

class MiniRedPostSearchForm(MongoSearchForm):
    search = CharField(required=False, max_length=20,
                       widget=TextInput(attrs={'class': 'form-control', 'placeholder': """Search Red Post..."""}))
    all = CharField(widget=HiddenInput, initial='S')

class RedPostDetailedSearchForm(MongoSearchForm):
    champions = MultipleChoiceField(choices=((c['name'], c['name']) for c in
                                    list(consumer.get_champions(projection={'name': 1}))),
                                    widget=CheckboxSelectMultiple, required=False, label="Champions")
    rioter = MultipleChoiceField(choices=itertools.chain(((item['name'], item['name']) for item in
                                    list(consumer.get_rioters(projection={'name': 1}))),), required=False,
                                    widget=SelectMultiple(attrs={'class': 'form-control'}),
                                    help_text="Hold Ctrl to select multiple Rioters in the list or unselect one.",
                                    label="Rioters")
    tags = MultipleChoiceField(choices=zip(ROLES+TAGS, ROLES+TAGS), required=False,
                                    widget=CheckboxSelectMultiple, label="Tags")
    section = MultipleChoiceField(choices=zip(ALL_SECTIONS, ALL_SECTIONS), required=False,
                                    widget=CheckboxSelectMultiple, label="Sections")
    region = MultipleChoiceField(choices=zip(REGIONS, REGIONS), required=False, widget=CheckboxSelectMultiple,
                                    label="Regions")
    date_before = DateTimeField(input_formats=DATE_FORMATS, widget=DateInput(attrs={'class': 'datePicker'}),
                                required=False, label="Posted before...", help_text="DD/MM/YYYY")
    date_after = DateTimeField(input_formats=DATE_FORMATS, widget=DateInput(attrs={'class': 'datePicker'}),
                               required=False, label="Posted after...", help_text="DD/MM/YYYY")
    search = CharField(required=False, max_length=20, label="Additional search", help_text="""Additional search in
                            post contents or thread title. If "match all" is unchecked, those won't be processed.""",
                            widget=TextInput(attrs={'class': 'form-control',
                                                    'placeholder': """Search in post contents or thread title..."""}))
    all = CharField(widget=HiddenInput, initial='S')
