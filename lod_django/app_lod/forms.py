import datetime
import itertools
import re
import string
from .models import STATUS, ARTICLE_TYPE, TAGS, ROLES, ALL_SECTIONS, REGIONS, DATE_FORMATS
from app_database.consumer import LoDConsumer
from bson import ObjectId
from django.forms import Form, CharField, ChoiceField, MultipleChoiceField, Textarea, HiddenInput, TextInput, \
                            DateTimeField, DateInput, BooleanField, CheckboxSelectMultiple, SelectMultiple
from random import choice
from utilities.mixins import MongoSearchForm

consumer = LoDConsumer('lod')

void_field = (('None', '--- None ---'),)
objectid_re = re.compile(r'^[a-f\d]{24}$')

class ChampionForm(Form):
    _id = CharField(widget=HiddenInput)
    summary = CharField(widget=Textarea)
    status = ChoiceField(choices=STATUS)

    def save(self):
        if hasattr(self, 'cleaned_data'):
            c_id = self.cleaned_data.pop('_id', None)
            return consumer.update('mr_champions', {'_id': ObjectId(c_id)}, {'$set': self.cleaned_data})

    def is_valid(self):
        return super(Form, self).is_valid() and objectid_re.match(self.cleaned_data['_id'])

class NewArticleForm(Form):
    _id = CharField(widget=HiddenInput)
    title = CharField(required=True, min_length=9, widget=TextInput(attrs={'size': '60'}))
    url_id = CharField(required=False, widget=TextInput(attrs={'size': '60'}))
    author = CharField()
    champion = ChoiceField(choices=itertools.chain(void_field, ((c['name'], c['name']) for c in
                                    list(consumer.get('mr_champions', projection={'name': 1}, sort_field="name"))),))
    type = ChoiceField(choices=ARTICLE_TYPE, required=True, initial='General')
    contents = CharField(required=True, widget=Textarea(attrs={'cols': '120', 'rows': 20}))

    def setup(self):
        if hasattr(self, 'cleaned_data'):
            if self.cleaned_data['url_id'] in [None, '', 'new']:
                new_url = re.sub(' +', '-', re.sub(r'[^a-zA-Z0-9: ]', '', self.cleaned_data['title'])).strip('-')
                if new_url == 'new':
                    new_url = 'PLZ-CHANGE-URL-'+''.join(choice(string.ascii_lowercase+string.digits)
                                                        for _ in range(1, 15))
                self.cleaned_data['url_id'] = new_url
            self.cleaned_data['date_modified'] = datetime.datetime.utcnow()
            if self.cleaned_data['_id'] == "new":
                self.cleaned_data['date_created'] = datetime.datetime.utcnow()

    def save(self):
        if hasattr(self, 'cleaned_data'):
            article_id = self.cleaned_data.pop('_id', None)
            if article_id == "new":
                query = {'url_id': self.cleaned_data['url_id']}
            else:
                query = {'_id': ObjectId(article_id)}
            return consumer.update_article(query, {'$set': self.cleaned_data})
        else:
            return None

    def is_valid(self):
        return super().is_valid() and objectid_re.match(self.cleaned_data['_id']) or self.cleaned_data['_id'] == "new"

class ArticleForm(NewArticleForm):
    _id = CharField(widget=HiddenInput)

    def is_valid(self):
        return super(NewArticleForm, self).is_valid()

class MiniRedPostSearchForm(MongoSearchForm):
    search = CharField(required=False, max_length=20,
                       widget=TextInput(attrs={'class': 'form-control', 'placeholder': """Search Red Post..."""}))

class RedPostDetailedSearchForm(MongoSearchForm):
    champions = MultipleChoiceField(choices=((c['name'], c['name']) for c in
                                    list(consumer.get('mr_champions', projection={'name': 1}, sort_field='name',))),
                                    widget=CheckboxSelectMultiple, required=False, label="Champions")
    rioter = MultipleChoiceField(choices=((item['name'], item['name']) for item in
                                    list(consumer.get('mr_rioters', projection={'name': 1}, sort_field='name',))), required=False,
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
    thread_id = CharField(required=False, label="Thread", widget=TextInput(attrs={'class': 'form-control',
                                                    'placeholder': """Search a specific thread or post ID..."""}),
                        help_text="""Look for a specific thread ID using its ID. It looks like '3Evd2LfW'.""")
