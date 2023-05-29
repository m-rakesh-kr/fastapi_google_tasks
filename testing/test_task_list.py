import json

"""---------------------------------------------------------------------------------"""
"""
Below are the Test Cases of Task list;
+ve Test Cases : Return --> Json Response                                       - 1 Nos
-ve Test Cases : Raises --> HTTP Exception Error Messages                       - 4 Nos

test_create_task_list_200: return created task_list                              : 201
test_create_task_list_incorrect_access_token: return 'Not authenticated'         : 401
test_show_all_task_list_200: return all the task list                            : 200 
test_show_all_task_list_incorrect_access_token: return 'Not authenticated'       : 401
test_show_one_task_list_200: return task_list with provided id                   : 200
test_show_one_task_list_not_found: return Task list Not found with details       : 404
test_update_task_list_200 : return update status message                         : 200
test_update_task_list_list_id_not_found: return Not found with details           : 404
test_delete_task_list_200: return delete status message                          : 200
test_delete_task_list_list_id_not_found: return Not Found with details
"""
"""----------------------------------------------------------------------------------"""


# def test_create_task_list_200(client, token_header):
#     data = {
#         "list_name": "My List"
#     }
#     response = client.post('/api/v1/create/task_list', data=json.dumps(data), headers={"authorization": token_header})
#     # print(f"RETURN{response.json()}")
#     assert response.status_code == 201
#     assert response.json()["list_name"] == data["list_name"]


def test_create_task_list_incorrect_access_token(client):
    data = {
        "list_name": "My List"
    }
    response = client.post('/api/v1/create/task_list', data=json.dumps(data),
                           headers={"authorization": "bcehbeqbisnaizkniqk"})
    # print(f"RETURN{response.json()}")
    assert response.status_code == 401
    assert response.json()["detail"] == 'Not authenticated'


def test_show_all_task_list_200(client, token_header):
    response = client.get('/api/v1/get_all/task_list', headers={"authorization": token_header})
    # print(f"RETURN{response.json()}")
    assert response.status_code == 200


def test_show_all_task_list_incorrect_access_token(client):
    response = client.get('/api/v1/get_all/task_list', headers={"authorization": "uwvcccccuvcwuevcuewcuevuwvucww"})
    # print(f"RETURN{response.json()}")
    assert response.status_code == 401
    assert response.json()["detail"] == 'Not authenticated'


def test_show_one_task_list_200(client, token_header):
    response = client.get('/api/v1/get_one/1/task_list', headers={"authorization": token_header})
    # print(f"RETURN{response.json()}")
    assert response.status_code == 200
    assert response.json()["id"] == '1'


def test_show_one_task_list_not_found(client, token_header):
    response = client.get('/api/v1/get_one/2/task_list', headers={"authorization": token_header})
    # print(f"RETURN{response.json()}")
    assert response.status_code == 404
    assert response.json()["detail"] == 'There is no any task list of task list id 2'


def test_update_task_list_200(client, token_header):
    data = {
        "list_name": "Updated List"
    }
    response = client.put('/api/v1/update/1/task_list', data=json.dumps(data), headers={"authorization": token_header})
    # print(f"RETURN{response.json()}")
    assert response.status_code == 200
    assert response.json()["message"] == 'Task list updated Successfully'


def test_update_task_list_list_id_not_found(client, token_header):
    data = {
        "list_name": "Updated List"
    }
    response = client.put('/api/v1/update/2/task_list', data=json.dumps(data), headers={"authorization": token_header})
    # print(f"RETURN{response.json()}")
    assert response.status_code == 404
    assert response.json()["detail"] == 'There is no any task list of task list id 2'


def test_delete_task_list_list_id_not_found(client, token_header):
    response = client.delete('/api/v1/delete/2/task_list', headers={"authorization": token_header})
    # print(f"RETURN{response.json()}")
    assert response.status_code == 404
    assert response.json()["detail"] == 'There is no any task list of task list id 2'


def test_delete_task_list_200(client, token_header):
    response = client.delete('/api/v1/delete/1/task_list', headers={"authorization": token_header})
    print(f"RETURN{response.json()}")
    assert response.status_code == 200
    assert response.json()["message"] == 'Task list deleted Successfully'
