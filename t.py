import database
# import hashlib

d = database.dbase()

d.start_db()
#d.delete_tables()

# print(b'a')
# print('a'.encode())

# m = hashlib.sha256(b'hi!')
# x = m.hexdigest()
#
# test = input()
# tm = hashlib.sha256()
# tm.update(test.encode())
# tx = tm.hexdigest()
# if tx == x:
#     print('xd')
# else:
#     print('no')
#
# print(x)
