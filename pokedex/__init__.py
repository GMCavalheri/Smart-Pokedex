import pymysql

# PyMySQL is a pure-Python MySQL driver: it needs no native build tools
# (unlike mysqlclient), so it installs the same way on every OS and inside
# Docker without extra system packages. Django only knows how to talk to
# MySQL through the MySQLdb API, so this line makes PyMySQL answer to that name.
# Django also checks the driver's reported version against mysqlclient's
# version scheme, so PyMySQL needs to report one high enough to pass.
pymysql.version_info = (2, 2, 4, "final", 0)
pymysql.install_as_MySQLdb()
