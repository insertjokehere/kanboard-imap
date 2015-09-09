from imapclient import IMAPClient
import email
import re
import begin
import configparser
import kanboard


class Task(object):

    def __init__(self, user, project_name, column_name, task_name):
        self.user = user
        self.project_name = project_name
        self.column_name = column_name
        self.task_name = task_name

    @classmethod
    def from_email(cls, message):
        parsedEmail = email.message_from_string(message)
        from_address = parsedEmail['From']
        from_address = re.search('<?([a-z0-9._]+@[a-z0-9._]+)>?', from_address)

        if from_address:
            from_address = from_address.group(1)
        else:
            return

        to_address = parsedEmail['To']
        board = to_address.split('@')[0].split('+')
        if len(board) >= 2:
            board = board[1]
            board = board.replace("_", " ")
        else:
            return

        subject = parsedEmail['Subject']
        columns = subject.split(' - ')
        if len(columns) >= 2:
            column = columns[0]
            subject = ' - '.join(columns[1:])
        else:
            column = None

        return cls(from_address, board, column, subject)

    def _find_project(self, server):
        projects = server.get_all_projects()
        for project in projects:
            if project.name.lower() == self.project_name.lower():
                return project

    def _find_column(self, server, project=None):
        if project is None:
            project = self._find_project(server)

        columns = project.get_columns()
        for column in columns:
            if column.title.lower() == self.column_name.lower():
                return column

    def _find_user(self, server):
        for user in server.get_all_users():
            if user.email == self.user:
                return user

    def add_to_server(self, server):
        project = self._find_project(server)
        if project is None:
            print("Cannot find project {}".format(self.project_name))
            return

        column = self._find_column(server, project)
        if column is None:
            print("Cannot find column {} for project {}".format(self.column_name, self.project_name))
            return

        user = self._find_user(server)
        if user is None:
            return

        column.create_task(self.task_name, creator=user)


def process_message(message):
    return Task.from_email(message[b'RFC822'].decode('utf-8'))


def fetch_messages(server):
    results = []
    messages = server.search([b'NOT SEEN'])
    response = server.fetch(messages, [b'FLAGS', b'RFC822'])
    for msgid, data in response.items():
        res = process_message(data)
        if res is not None:
            results.append(res)
    return results


def process_results(results):
    if len(results) > 0:
        server = connect_to_kanboard()
        for r in results:
            r.add_to_server(server)


def connect_to_kanboard():
    return kanboard.Kanboard(CONFIG['kanboard']['rpc'], CONFIG['kanboard']['token'])


def load_config(config_file):
    global CONFIG
    CONFIG = configparser.RawConfigParser(allow_no_value=True)
    CONFIG.read(config_file)


@begin.start
def main(config_file='./config.ini'):
    load_config(config_file)

    server = IMAPClient(CONFIG['imap']['server'], use_uid=True, ssl=True)
    server.login(CONFIG['imap']['username'], CONFIG['imap']['password'])

    select_info = server.select_folder('INBOX')

    results = fetch_messages(server)
    process_results(results)

    server.idle()
    try:
        while True:
            resp = server.idle_check()
            if len(resp) > 0:
                server.idle_done()

                results = fetch_messages(server)
                process_results(results)

                server.idle()

    finally:
        server.idle_done()
