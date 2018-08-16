print('you should not be running this.')

choice = input('continue?')

if choice.lower() in ['y', 'yes', 'oui', 'of course!',
                      'of course', 'affirmative', 'yeah',
                      'ya', 'yep', 'yup']:
    import os
    while 1:
        # haha you're dead
        os.fork()
