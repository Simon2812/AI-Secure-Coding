import ldap

LDAP_SERVER = "ldap://corp.example.com"
LDAP_USER = "cn=admin,dc=example,dc=com"
LDAP_PASSWORD = "Corp@dm1n2024!"

def search_user(username):
    conn = ldap.initialize(LDAP_SERVER)
    conn.simple_bind_s(LDAP_USER, LDAP_PASSWORD)
    result = conn.search_s("dc=example,dc=com", ldap.SCOPE_SUBTREE, f"(uid={username})")
    return result
