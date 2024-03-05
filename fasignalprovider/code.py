from enum import Enum

class Code(Enum):

    def __init__(self, code, message):
        self.code = code
        self.message = message

    def __str__(self):
        return f"{self.code} {self.message}"

    # 2xx Success
    OK = (200, "OK: The request has succeeded.")
    CREATED = (201, "Created: The request has been fulfilled and resulted in a new resource being created.")
    ACCEPTED = (202, "Accepted: The request has been accepted for processing, but the processing has not been completed.")
    NON_AUTHORITATIVE_INFORMATION = (203, "Non-Authoritative Information: The request was successful but the enclosed payload has been modified from that of the origin server's 200 OK response by a transforming proxy.")
    NO_CONTENT = (204, "No Content: The server successfully processed the request and is not returning any content.")
    RESET_CONTENT = (205, "Reset Content: The server successfully processed the request, but is not returning any content. Unlike a 204 response, this response requires that the requester reset the document view.")
    PARTIAL_CONTENT = (206, "Partial Content: The server is delivering only part of the resource due to a range header sent by the client.")
    MULTI_STATUS = (207, "Multi-Status: Provides status for multiple independent operations.")
    ALREADY_REPORTED = (208, "Already Reported: Used inside a DAV: propstat response element to avoid enumerating the internal members of multiple bindings to the same collection repeatedly.")
    IM_USED = (226, "IM Used: The server has fulfilled a GET request for the resource, and the response is a representation of the result of one or more instance-manipulations applied to the current instance.")

    # 4xx Client Errors
    BAD_REQUEST = (400, "Bad Request: The server could not understand the request due to invalid syntax.")
    UNAUTHORIZED = (401, "Unauthorized: The client must authenticate itself to get the requested response.")
    FORBIDDEN = (403, "Forbidden: The client does not have access rights to the content.")
    NOT_FOUND = (404, "Not Found: The server can not find the requested resource.")
    METHOD_NOT_ALLOWED = (405, "Method Not Allowed: The method specified in the request is not allowed.")
    NOT_ACCEPTABLE = (406, "Not Acceptable: The server cannot produce a response matching the list of acceptable values defined in the request's proactive content negotiation headers.")
    PROXY_AUTHENTICATION_REQUIRED = (407, "Proxy Authentication Required: The client must first authenticate itself with the proxy.")
    REQUEST_TIMEOUT = (408, "Request Timeout: The server timed out waiting for the request.")
    CONFLICT = (409, "Conflict: The request could not be processed because of conflict in the request, such as an edit conflict.")
    GONE = (410, "Gone: The content requested has been permanently deleted from server, with no forwarding address.")
    LENGTH_REQUIRED = (411, "Length Required: The server rejects the request because the Content-Length header field is not defined and the server requires it.")
    PRECONDITION_FAILED = (412, "Precondition Failed: The server does not meet one of the preconditions that the requester put on the request.")
    PAYLOAD_TOO_LARGE = (413, "Payload Too Large: The request entity is larger than limits defined by server.")
    URI_TOO_LONG = (414, "URI Too Long: The URI requested by the client is longer than the server is willing to interpret.")
    UNSUPPORTED_MEDIA_TYPE = (415, "Unsupported Media Type: The media format of the requested data is not supported by the server, so the server is rejecting the request.")
    RANGE_NOT_SATISFIABLE = (416, "Range Not Satisfiable: The range specified by the Range header field in the request can't be fulfilled.")
    EXPECTATION_FAILED = (417, "Expectation Failed: The server cannot meet the requirements of the Expect request-header field.")
    IM_A_TEAPOT = (418, "I'm a teapot: The server refuses the attempt to brew coffee with a teapot.")
    MISDIRECTED_REQUEST = (421, "Misdirected Request: The request was directed at a server that is not able to produce a response.")
    UNPROCESSABLE_ENTITY = (422, "Unprocessable Entity: The server understands the content type of the request entity, and the syntax of the request entity is correct, but it was unable to process the contained instructions.")
    LOCKED = (423, "Locked: The resource that is being accessed is locked.")
    FAILED_DEPENDENCY = (424, "Failed Dependency: The request failed due to failure of a previous request.")
    TOO_EARLY = (425, "Too Early: Indicates that the server is unwilling to risk processing a request that might be replayed.")
    UPGRADE_REQUIRED = (426, "Upgrade Required: The server refuses to perform the request using the current protocol but might be willing to do so after the client upgrades to a different protocol.")
    PRECONDITION_REQUIRED = (428, "Precondition Required: The origin server requires the request to be conditional.")
    TOO_MANY_REQUESTS = (429, "Too Many Requests: The user has sent too many requests in a given amount of time.")
    REQUEST_HEADER_FIELDS_TOO_LARGE = (431, "Request Header Fields Too Large: The server is unwilling to process the request because its header fields are too large.")
    UNAVAILABLE_FOR_LEGAL_REASONS = (451, "Unavailable For Legal Reasons: The server is denying access to the resource as a consequence of a legal demand.")

    # 5XX Server Errors
    INTERNAL_SERVER_ERROR = (500, "Internal Server Error: The server encountered an unexpected condition.")
    NOT_IMPLEMENTED = (501, "Not Implemented: The server does not support the functionality required to fulfill the request.")
    BAD_GATEWAY = (502, "Bad Gateway: The server received an invalid response from the upstream server.")
    SERVICE_UNAVAILABLE = (503, "Service Unavailable: The server is currently unable to handle the request due to temporary overloading or maintenance.")
    GATEWAY_TIMEOUT = (504, "Gateway Timeout: The server did not receive a timely response from the upstream server.")
    HTTP_VERSION_NOT_SUPPORTED = (505, "HTTP Version Not Supported: The server does not support the HTTP protocol version used in the request.")
    VARIANT_ALSO_NEGOTIATES = (506, "Variant Also Negotiates: Transparent content negotiation for the request results in a circular reference.")
    INSUFFICIENT_STORAGE = (507, "Insufficient Storage: The server is unable to store the representation needed to complete the request.")
    LOOP_DETECTED = (508, "Loop Detected: The server detected an infinite loop while processing the request.")
    NOT_EXTENDED = (510, "Not Extended: Further extensions to the request are required for the server to fulfill it.")
    NETWORK_AUTHENTICATION_REQUIRED = (511, "Network Authentication Required: The client needs to authenticate to gain network access.")

    
