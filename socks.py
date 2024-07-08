import socket
import ast
from config import env


def send_data_through_socks_proxy(data, num, logger):
    """
    Send data through socks to the Host and Port established in configuration.
    Returns the response from the server and converts it to a list of tuples
    """

    all_chains = []
    for i in range(num):
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            host = env.get("HOST")
            port = env.get("PORT")
            if host is None or port is None:
                raise ValueError("Please enter a valid HOST and PORT in the config file.")
            server_address = (host, port)
            client_socket.connect(server_address)
        except (KeyError, ValueError, ConnectionError) as e:
            logger.error(str(e))
            return

        client_socket.send(str(data[i]).encode('utf-8'))

        response_by_chain = client_socket.recv(4096000000).decode()

        list_of_tuples = convert_response(response_by_chain)
        all_chains.append(list_of_tuples[0])

    client_socket.close()
    return all_chains


def convert_response(response):
    """
    Convert the response string into a list of tuples
    """

    modified_str = response.replace("[(<class 'float'>, <class 'str'>), ", "[")
    list_of_tuples = ast.literal_eval(modified_str)
    return list_of_tuples
