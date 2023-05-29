import json

"""---------------------------------------------------------------------------------"""
"""
Below are the Test Cases of Sub_Task;
+ve Test Cases : Return --> Json Response                                        - 1 Nos
-ve Test Cases : Raises --> HTTP Exception Error Messages                        - 4 Nos
test_create_sub_task_200: return created sub_task                                : 201
test_create_sub_task_of_not_found_task: return Not found message                 : 404
test_create_sub_task_incorrect_access_token: return 'Not authenticated'          : 401
test_show_all_sub_task_200: return all the sub_task list                         : 200
test_show_all_sub_task_of_not_found_sub_task_list: return Not found message      : 404
test_show_all_sub_task_incorrect_access_token: return 'Not authenticated'        : 401
test_show_one_sub_task_200: return sub_task with provided id                     : 200
test_show_one_sub_task_not_found: return sub_task list Not found with details    : 404
test_update_sub_task_200 : return update status message                          : 200
test_update_sub_task_id_not_found: return Not found with details                 : 404
test_delete_sub_task_200: return delete status message                           : 200
test_delete_sub_task_id_not_found: return Not Found with details                 : 404 
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


def test_create_task_demo(client, token_header):
    data = {
        "title": "Demo my task",
        "details": "This is a details of Demo my task",
        "date_time": "2022-08-30T07:12:52.490000"
    }
    response = client.post('/api/v1/create/1/task', data=json.dumps(data), headers={"authorization": token_header})
    # print(f"RETURN{response.json()}")
    assert response.status_code == 201
    assert response.json()["id"] == 1
    assert response.json()["title"] == data['title']
    assert response.json()["details"] == data['details']
    assert response.json()["date_time"] == data['date_time']


def test_create_sub_task_200(client, token_header):
    data = {
        "title": "My sub_task",
        "details": "This is a details of my sub_task",
        "date_time": "2022-08-30T07:12:52.490000"
    }
    response = client.post('/api/v1/create/1/sub_task', data=json.dumps(data), headers={"authorization": token_header})
    # print(f"RETURN{response.json()}")
    assert response.status_code == 201
    assert response.json()["id"] == 1
    assert response.json()["title"] == data['title']
    assert response.json()["details"] == data['details']
    assert response.json()["date_time"] == data['date_time']


def test_create_sub_task_of_not_found_task(client, token_header):
    data = {
        "title": "My sub_task2",
        "details": "This is a details of my sub_task2",
        "date_time": "2022-08-30T07:12:52.490000"
    }
    response = client.post('/api/v1/create/2/sub_task', data=json.dumps(data),
                           headers={"authorization": token_header})
    # print(f"RETURN{response.json()}")
    assert response.status_code == 404
    assert response.json()["detail"] == 'There is no any task of task id 2'


def test_create_sub_task_incorrect_access_token(client):
    data = {
        "title": "My sub_task",
        "details": "This is a details of my sub_task",
        "date_time": "2022-08-30T07:12:52.490000"
    }
    response = client.post('/api/v1/create/1/sub_task', data=json.dumps(data),
                           headers={"authorization": "bcehbeqbisnaizkniqk"})
    # print(f"RETURN{response.json()}")
    assert response.status_code == 401
    assert response.json()["detail"] == 'Not authenticated'


def test_show_all_sub_task_200(client, token_header):
    response = client.get('/api/v1/get_all/1/sub_task', headers={"authorization": token_header})
    # print(f"RETURN{response.json()}")
    assert response.status_code == 200


def test_show_all_sub_task_of_not_found_task(client, token_header):
    response = client.get('/api/v1/get_all/2/sub_task', headers={"authorization": token_header})
    # print(f"RETURN{response.json()}")
    assert response.status_code == 404
    assert response.json()["detail"] == 'There is no any sub task of task id 2'


def test_show_all_sub_task_incorrect_access_token(client):
    response = client.get('/api/v1/get_all/1/sub_task', headers={"authorization": "uwvcccccuvcwuevcuewcuevuwvucww"})
    # print(f"RETURN{response.json()}")
    assert response.status_code == 401
    assert response.json()["detail"] == 'Not authenticated'


def test_show_one_sub_task_200(client, token_header):
    response = client.get('/api/v1/get_one/1/sub_task', headers={"authorization": token_header})
    # print(f"RETURN{response.json()}")
    assert response.status_code == 200
    assert response.json()["id"] == '1'


def test_show_one_sub_task_not_found(client, token_header):
    response = client.get('/api/v1/get_one/2/sub_task', headers={"authorization": token_header})
    # print(f"RETURN{response.json()}")
    assert response.status_code == 404
    assert response.json()["detail"] == 'There is no any sub task of sub task id 2'


def test_update_sub_task_200(client, token_header):
    data = {
        "title": "Updated My sub_task",
        "details": "This is a details of updated my sub_task",
        "date_time": "2022-08-30T07:12:52.490000"
    }
    response = client.put('/api/v1/update/1/sub_task', data=json.dumps(data), headers={"authorization": token_header})
    # print(f"RETURN{response.json()}")
    assert response.status_code == 200
    assert response.json()["message"] == 'Sub task updated Successfully'


def test_update_sub_task_id_not_found(client, token_header):
    data = {
        "title": "Updated My sub_task",
        "details": "This is a details of updated my sub_task",
        "date_time": "2022-08-30T07:12:52.490000"
    }
    response = client.put('/api/v1/update/2/sub_task', data=json.dumps(data), headers={"authorization": token_header})
    # print(f"RETURN{response.json()}")
    assert response.status_code == 404
    assert response.json()["detail"] == 'There is no any sub task of sub task id 2'


def test_delete_sub_task_id_not_found(client, token_header):
    response = client.delete('/api/v1/delete/2/sub_task', headers={"authorization": token_header})
    # print(f"RETURN{response.json()}")
    assert response.status_code == 404
    assert response.json()["detail"] == 'There is no any sub task of sub task id 2'


def test_delete_sub_task_200(client, token_header):
    response = client.delete('/api/v1/delete/1/sub_task', headers={"authorization": token_header})
    # print(f"RETURN{response.json()}")
    assert response.status_code == 200
    assert response.json()["message"] == 'Sub task deleted Successfully'
