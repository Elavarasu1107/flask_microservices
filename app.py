from user.views import app as user
from notes.views import app as note

if __name__ == '__main__':
    user.run()
    note.run()
