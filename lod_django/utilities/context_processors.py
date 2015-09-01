from app_database.consumer import Consumer

consumer = Consumer()

def champions_list_data(request):
    return {'champions': [c for c in consumer.get_champions()]}