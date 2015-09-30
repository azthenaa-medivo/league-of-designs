from app_lod.forms import MiniRedPostSearchForm
from app_lod.models import REGIONS, GLORIOUS_SECTIONS
from app_database.consumer import Consumer

consumer = Consumer()

def champions_list_data(request):
    return {'champions': [c for c in consumer.get_champions()]}

def static_models_data(request):
    return {'regions': zip(REGIONS, REGIONS), 'glorious_sections': GLORIOUS_SECTIONS}

def navbar_search(request):
    return {'navbarsearch': MiniRedPostSearchForm()}