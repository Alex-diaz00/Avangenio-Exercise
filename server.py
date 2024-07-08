import socket
import re
from config import env
from log import logs


def contains_pattern(chain):
    """
    Returns whether the string contains any of these elements (aa, AA, aA, Aa)
    """

    # Define the regex pattern
    pattern = r"(a{2}|A{2}|aA|Aa)"

    # Search the chain for the pattern
    match = re.search(pattern, chain)

    # Check if a match was found
    return bool(match)


def count_elements(chain):
    """
    Counts the number of letters, numbers and spaces that a chain has
    """

    letters = 0
    numbers = 0
    spaces = 0

    for char in chain:
        if char.isalpha():
            letters += 1
        elif char.isdigit():
            numbers += 1
        elif char.isspace():
            spaces += 1

    return letters, numbers, spaces


def calculate_weight(chain, logger):
    """
    Calculates the weight of a chain. If the chain contains some of these
    elements (aa, AA, aA, Aa) then the weight is 1000
    """

    if not contains_pattern(chain):
        letters, numbers, spaces = count_elements(chain)
        logger.info(f"Letters: {letters}    Numbers: {numbers}    Spaces: {spaces}")
        return (letters * 1.5 + numbers * 2) / spaces
    else:
        logger.info(f"Double 'a' rule detected >> '{chain}'")
        return 1000


def run_server():
    """
    Run the server
    """

    logger = logs("server.log")

    try:
        host = env.get("HOST")
        port = env.get("PORT")

        if host is None or port is None:
            raise ValueError("Please enter a valid HOST and PORT in the config file.")
    except (KeyError, ValueError) as e:
        logger.error(str(e))
        return
    # Create a socket object
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bind the socket to the address
    server_socket.bind((host, port))
    logger.info("Server is listening ...")

    while True:
        server_socket.listen()
        client_socket, addr = server_socket.accept()
        logger.info(f"Connection from {addr} has been established.")

        # Receive data from the client
        data = client_socket.recv(4096000000).decode()

        response = [(float, str)]
        weight = calculate_weight(data, logger)
        logger.info(f'Weight of the chain >>> "{weight}"')
        logger.info(f'Chain >>> "{data}"')
        response.append((weight, data))

        # Send the response back to the client
        client_socket.send(str(response).encode())

    client_socket.close()


run_server()
