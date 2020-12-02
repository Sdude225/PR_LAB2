import enum

class Header_Types(enum.Enum):
    header_size = 5
    ping = 'PING0'
    request_clients_numbers = 'RECLN'
    delete_number = 'DELNR'
    end_message = 'ENDMS'
    encrypted_end_message = 'EENDM'
    syn_message = 'SYNMS'
    syn_response = 'SYNRS'