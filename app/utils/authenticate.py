import jwt
from datetime import timedelta, datetime
from settings import GET
from app.models.users import UserHistory
from ldap3 import Server, Connection, SUBTREE, ALL


def authenticate_user(username: str, password: str):
    if username.endswith("com"):
        ldap_base_search = ("dc=company,dc=com", "192.168.1.1")
    else:
        return [False, f"{username} Invalid"]

    try:
        conn = Connection(Server(ldap_base_search[1], get_info=ALL),
                          user=username,
                          password=password,
                          authentication="SIMPLE",
                          client_strategy="SYNC")
    except Exception as err:
        return [False, f"Connection Error{err}"]

    res_bind = conn.bind()
    if not res_bind:
        return [False, ""]

    conn.search(search_base=ldap_base_search[0],
                search_filter='(&(objectCategory=Person)(sAMAccountName={}))'.format(
                    username[:username.find('@')]),
                search_scope=SUBTREE,
                attributes=['name', 'mail', 'sAMAccountName', 'sAMAccountType'])

    if conn.entries:
        resp_dict = {
            "name": str(conn.entries[0].name),
            "username": str(conn.entries[0].sAMAccountName),
            "email": str(conn.entries[0].mail)
        }
        return [True, resp_dict]


def create_access_token(*, data: dict, expire_time: timedelta = None):
    to_encode = data.copy()
    if expire_time:
        expire = expire_time + datetime.utcnow()
    else:
        expire = datetime.utcnow() + timedelta(days=7)

    to_encode.update({"exp": expire})
    token = jwt.encode(to_encode, GET.SECRET_KEY, GET.ALGORITHM)
    return token


def write_logs_to_db(request):
    logs_data = dict()
    logs_data["http_url"] = request.path
    logs_data["http_method"] = request.method
    logs_data["request_ip"] = request.remote_addr

    logs_obj = UserHistory.create(**logs_data)
    return logs_obj
