
"""
Example script showing how to represent todo lists and todo entries in Python
data structures and how to implement endpoint for a REST API with Flask.

Requirements:
* flask
"""

import uuid 

from flask import Flask, request, jsonify, abort


# initialize Flask server
app = Flask(__name__)

# create unique id for lists, entries
todo_list_1_id = '1318d3d1-d979-47e1-a225-dab1751dbe75'
todo_list_2_id = '3062dc25-6b80-4315-bb1d-a7c86b014c65'
todo_list_3_id = '44b02e00-03bc-451d-8d01-0c67ea866fee'
todo_1_id = uuid.uuid4()
todo_2_id = uuid.uuid4()
todo_3_id = uuid.uuid4()
todo_4_id = uuid.uuid4()

# define internal data structures with example data
todo_lists = [
    {'id': todo_list_1_id, 'name': 'Einkaufsliste'},
    {'id': todo_list_2_id, 'name': 'Arbeit'},
    {'id': todo_list_3_id, 'name': 'Privat'},
]
todos = [
    {'id': todo_1_id, 'name': 'Milch', 'description': '', 'list': todo_list_1_id},
    {'id': todo_2_id, 'name': 'Arbeitsblätter ausdrucken', 'description': '', 'list': todo_list_2_id},
    {'id': todo_3_id, 'name': 'Kinokarten kaufen', 'description': '', 'list': todo_list_3_id},
    {'id': todo_3_id, 'name': 'Eier', 'description': '', 'list': todo_list_1_id},
]

# add some headers to allow cross origin access to the API on this server, necessary for using preview in Swagger Editor!
@app.after_request
def apply_cors_header(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET,POST,DELETE,PATCH'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    return response

# define endpoint for getting and deleting existing todo lists
@app.route('/list/<list_id>', methods=['GET', 'DELETE'])
def handle_list(list_id):
    # find todo list depending on given list id
    list_item = None
    for l in todo_lists:
        if l['id'] == list_id:
            list_item = l
            break
    # if the given list id is invalid, return status code 404
    if not list_item:
        abort(404)
    if request.method == 'GET':
        # find all todo entries for the todo list with the given id
        print('Returning todo list...')
        return jsonify([i for i in todos if i['list'] == list_id]),200
    elif request.method == 'DELETE':
        # delete list with given id
        for l in todo_lists:
            if l['id'] == list_id:
                list_item = l
                break
        # if the given list id is invalid, return status code 404
        if not list_item:
            abort(404)
        print('Deleting todo list...')
        todo_lists.remove(list_item)
        return '', 200


# define endpoint for adding a new list
@app.route('/list', methods=['POST'])
def add_new_list():
    # make JSON from POST data (even if content type is not set correctly)
    new_list = request.get_json(force=True)
    if not new_list:
        abort(500)
    print('Got new list to be added: {}'.format(new_list))
    # create id for new list, save it and return the list with id
    new_list['id'] = str(uuid.uuid4())
    todo_lists.append(new_list)
    return jsonify(new_list), 200


# define endpoint for getting all lists
@app.route('/lists', methods=['GET'])
def get_all_lists():
    if not todo_lists:
        abort(500)  
    return jsonify(todo_lists), 200


@app.route('/list/<list_id>/item', methods=['POST'])
def add_item_to_list(list_id):
    list_item = next((l for l in todo_lists if l['id'] == list_id), None)
    if not list_item:
        abort(404)
    new_item = request.get_json(force=True)
    if not new_item:
        abort(500)
    new_item['id'] = str(uuid.uuid4())
    new_item['list'] = list_id
    todos.append(new_item)
    return jsonify(new_item), 200

@app.route('/list/<list_id>/item/<item_id>', methods=['DELETE'])
def delete_item_from_list(list_id, item_id):
    list_item = next((l for l in todo_lists if l['id'] == list_id), None)
    item = next((i for i in todos if i['id'] == item_id and i['list_id'] == list_id), None)
    if not list_item or not item:
        abort(404)
    todos.remove(item)
    return '', 200

@app.route('/list/<list_id>/item/<item_id>', methods=['PATCH'])
def update_item_in_list(list_id, item_id):
    list_item = next((l for l in todo_lists if l['id'] == list_id), None)
    item = next((i for i in todos if i['id'] == item_id and i['list_id'] == list_id), None)
    if not list_item or not item:
        abort(404)
    update_data = request.get_json(force=True)
    item.update(update_data)
    return jsonify(item), 200

@app.route('/list/<list_id>', methods=['PATCH'])
def update_name(list_id):
    list_item = next((l for l in todo_lists if l['id'] == list_id), None)
    if not list_item:
        abort(404)
    new_name = request.get_json(force=True)
    new_list_name = new_name['name']
    list_item["name"] = new_list_name
    return jsonify(list_item), 200

if __name__ == '__main__':
    # start Flask server
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
