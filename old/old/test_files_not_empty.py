# import pytest
# import os
# import sys


# def files_not_empty(root_dir):
#     path = os.path.join(os.getcwd(), root_dir)
#     print('\n\nfiles under ' + root_dir + '\n\n')
#     for (path, dirs, files) in os.walk(path):
#         for f in files:
#             fp = os.path.join(path, f)
#             size = os.path.getsize(fp)
#             print(fp)
#             print('size: ' + str(size) + ('' if size != 0 else '        ****empty****'))

#     return True


# def test_server(serverFiles):
#     assert files_not_empty(serverFiles.root_dir) is True


# def test_client(clientFiles):
#     assert files_not_empty(clientFiles.root_dir) is True
