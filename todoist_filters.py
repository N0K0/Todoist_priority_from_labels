import todoist

secret = 'API_KEY_HERE'

api = todoist.api.TodoistAPI(secret)
api.sync_token='*' #  Full sync is needed
response = api.sync()

print(api,response)

labels = {'Not_Important': 0,
          'Not_urgent': 0,
          'Important': 0,
          'Urgent':0}


values = {'Not_Important': 0,
          'Not_urgent': 0,
          'Important': 2,
          'Urgent':1}

# Getting the label id's to check later
for label in response['labels']:
    name = label['name']
    id = label['id']
    labels[name] = id

assert len(labels) == 4, "Something wierd with the labels"

# Lets iterate over the items and tag those we like
def get_label_from_id(id):
    for label in labels.keys():
        value = labels[label]
        if value == id:
            return label

    return "Not applicable"

#Setting the pri
for number,item in enumerate(response['items'],start=1):
    pri = 1
    item_labels = item['labels']
    debug = []
    for label_id in item_labels:
        label_name = get_label_from_id(label_id)
        pri += values[label_name]
        debug.append(label_name)

    print(debug)
    print(pri)
    api.items.update(item['id'],priority=pri)
    if number % 25 == 0:
        api.commit()
api.commit()
