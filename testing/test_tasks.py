import json

"""---------------------------------------------------------------------------------"""
"""
Below are the Test Cases of Task;
+ve Test Cases : Return --> Json Response                                       - 1 Nos
-ve Test Cases : Raises --> HTTP Exception Error Messages                       - 4 Nos
test_create_task_200: return created task                                       : 201
test_create_task_of_not_found_task_list: return Not found message               : 404
test_create_task_incorrect_access_token: return 'Not authenticated'             : 401
test_show_all_task_200: return all the task list                                : 200
test_show_all_task_of_not_found_task_list: return Not found message             : 404
test_show_all_task_incorrect_access_token: return 'Not authenticated'           : 401
test_show_one_task_200: return task with provided id                            : 200
test_show_one_task_not_found: return Task list Not found with details           : 404
test_update_task_200 : return update status message                             : 200
test_update_task_id_not_found: return Not found with details                    : 404
test_delete_task_200: return delete status message                              : 200
test_delete_task_id_not_found: return Not Found with details                    : 404 
"""
"""----------------------------------------------------------------------------------"""


def test_create_task_list_demo(client, token_header):
    data = {
        "list_name": "Demo Task List"
    }
    response = client.post('/api/v1/create/task_list', data=json.dumps(data), headers={"authorization": token_header})
    # print(f"RETURN{response.json()}")
    assert response.status_code == 201
    assert response.json()["list_name"] == data["list_name"]


def test_create_task_200(client, token_header):
    data = {
        "title": "My task",
        "details": "This is a details of my task",
        "date_time": "2022-08-30T07:12:52.490000"
    }
    response = client.post('/api/v1/create/1/task', data=json.dumps(data), headers={"authorization": token_header})
    print(f"RETURN{response.json()}")
    assert response.status_code == 201
    assert response.json()["id"] == 2
    assert response.json()["title"] == data['title']
    assert response.json()["details"] == data['details']
    assert response.json()["date_time"] == data['date_time']


def test_create_task_of_not_found_task_list(client, token_header):
    data = {
        "title": "My task2",
        "details": "This is a details of my task2",
        "date_time": "2022-08-30T07:12:52.490000"
    }
    response = client.post('/api/v1/create/5/task', data=json.dumps(data),
                           headers={"authorization": token_header})
    # print(f"RETURN{response.json()}")
    assert response.status_code == 404
    assert response.json()["detail"] == 'User have not any task list of id 5'


def test_create_task_incorrect_access_token(client):
    data = {
        "title": "My task",
        "details": "This is a details of my task",
        "date_time": "2022-08-30T07:12:52.490000"
    }
    response = client.post('/api/v1/create/1/task', data=json.dumps(data),
                           headers={"authorization": "bcehbeqbisnaizkniqk"})
    # print(f"RETURN{response.json()}")
    assert response.status_code == 401
    assert response.json()["detail"] == 'Not authenticated'


def test_show_all_task_200(client, token_header):
    response = client.get('/api/v1/get_all/1/task', headers={"authorization": token_header})
    # print(f"RETURN{response.json()}")
    assert response.status_code == 200


def test_show_all_task_of_not_found_task_list(client, token_header):
    response = client.get('/api/v1/get_all/5/task', headers={"authorization": token_header})
    # print(f"RETURN{response.json()}")
    assert response.status_code == 404
    assert response.json()["detail"] == 'User have not any task list of id 5'


def test_show_all_task_incorrect_access_token(client):
    response = client.get('/api/v1/get_all/1/task', headers={"authorization": "uwvcccccuvcwuevcuewcuevuwvucww"})
    # print(f"RETURN{response.json()}")
    assert response.status_code == 401
    assert response.json()["detail"] == 'Not authenticated'


def test_show_one_task_200(client, token_header):
    response = client.get('/api/v1/get_one/1/task', headers={"authorization": token_header})
    # print(f"RETURN{response.json()}")
    assert response.status_code == 200
    assert response.json()["id"] == '1'


def test_show_one_task_not_found(client, token_header):
    response = client.get('/api/v1/get_one/5/task', headers={"authorization": token_header})
    # print(f"RETURN{response.json()}")
    assert response.status_code == 404
    assert response.json()["detail"] == 'There is no any task of task id 5'


def test_update_task_200(client, token_header):
    data = {
        "title": "Updated My task",
        "details": "This is a details of updated my task",
        "date_time": "2022-08-30T07:12:52.490000"
    }
    response = client.put('/api/v1/update/1/task', data=json.dumps(data), headers={"authorization": token_header})
    # print(f"RETURN{response.json()}")
    assert response.status_code == 200
    assert response.json()["message"] == 'Task updated Successfully'


def test_update_task_id_not_found(client, token_header):
    data = {
        "title": "Updated My task",
        "details": "This is a details of updated my task",
        "date_time": "2022-08-30T07:12:52.490000"
    }
    response = client.put('/api/v1/update/5/task', data=json.dumps(data), headers={"authorization": token_header})
    # print(f"RETURN{response.json()}")
    assert response.status_code == 404
    assert response.json()["detail"] == 'There is no any task of task id 5'


def test_delete_task_id_not_found(client, token_header):
    response = client.delete('/api/v1/delete/5/task', headers={"authorization": token_header})
    # print(f"RETURN{response.json()}")
    assert response.status_code == 404
    assert response.json()["detail"] == 'There is no any task of task id 5'


def test_delete_task_200(client, token_header):
    response = client.delete('/api/v1/delete/1/task', headers={"authorization": token_header})
    # print(f"RETURN{response.json()}")
    assert response.status_code == 200
    assert response.json()["message"] == 'Task deleted Successfully'
