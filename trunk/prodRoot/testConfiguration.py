import os

defaultValueDbDir = 'D:/tagfs/defaultTestValueDbPath/'

defaultValueDbPath = defaultValueDbDir+'value.sqlite'
defaultTokenDbPath = defaultValueDbDir+'token.sqlite'
g_thumbnail_dir = defaultValueDbDir+'/thumb/'
g_encrypted_file_dir = os.path.join(defaultValueDbDir,'encrypted')
g_private_file_dir = os.path.join(defaultValueDbDir,'removeAfterExit')
g_default_object_wait_time = 0
g_default_send_mailbox_server = ''
g_default_send_mailbox_user = ''
g_default_send_mailbox_pass = ''
g_default_receive_mailbox_server = ''
g_default_receive_mailbox_user = ''
g_default_receive_mailbox_pass = ''
g_default_receive_mailbox_server2 = ''
g_default_receive_mailbox_user2 = ''
g_default_receive_mailbox_pass2 = ''

g_encrypted_file_dir = 'D:/tagfs/encrypted'

g_default_database_server = 'http://127.0.0.1:8801/'
g_default_database_server_url = g_default_database_server+'app/'

g_default_proxy = {}
g_default_ufs_database_value_db_path = defaultValueDbDir+'adminValueDb.sqlite'
g_default_ufs_database_token_db_path = defaultValueDbDir+'adminTokenDb.sqlite'
g_default_database_root_path = defaultValueDbDir
g_default_webserver_port = 8801
g_default_xmlrpc_port = 8891
g_default_database_schema_remote = True
g_default_user_tag_db_name = 'userTagDb'
g_firefox_down_pic_remove = False