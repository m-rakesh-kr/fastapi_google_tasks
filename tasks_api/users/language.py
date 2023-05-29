from fastapi.encoders import jsonable_encoder


def convert_data_into_json(request_data):
    """
    This method is converted request data into json format.
    :param request_data: request data
    :return: Json data
    """
    return jsonable_encoder(request_data)


def send_success_response(status_code, message, data):
    """
   Return success response with status RESPONSE_STATUS_SUCCESS
   :return: success response
   """
    response = {'message': message or 'Success', "data": data}
    return response, status_code
