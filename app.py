from user.views import app as user
from notes.views import app as note
from labels.views import app as label

if __name__ == '__main__':
    user.run()
    note.run()
    label.run()
