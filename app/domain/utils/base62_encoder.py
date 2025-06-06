import uuid

def parse_number_to_base62(n: int) -> str:
    '''
    Primero recibimos un UUID4 parseado a INT. Luego, cada uno de sus caracteres 
    corresponde a una posicion en los posibles caracteres de la base62. Finalmente,
    se concatenan los caracteres seleccionados y se forma el hash_id.
    '''
    
    CURRENT_BASE = 62
    BASE62_ALPHABET = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
    
    if not isinstance(n, int): 
        raise TypeError("unable to encode a type different to integer")
    
    if n == 0:
        return BASE62_ALPHABET[n]
    
    char_list = []
    
    while n:
        n, rem = divmod(n, CURRENT_BASE)
        char_list.append(BASE62_ALPHABET[rem])
    return "".join(reversed(char_list))
        
    
def generate_random_short_id() -> str:
    WISHED_LENGTH = 12
    uuid_to_encode = uuid.uuid4().int
    base62_id = parse_number_to_base62(uuid_to_encode)
    return base62_id[:WISHED_LENGTH]