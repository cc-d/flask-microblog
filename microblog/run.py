#!/usr/bin/env python3
def main(port=80):
    from sys import argv

    from website import app as app

    try:
        app.run(host='0.0.0.0', port=argv[1])
    except IndexError:
        stars = '\n' + (20 * '*') + '\n'
        print(stars + 'No port found, using default port %s' % port + stars)
        app.run(host='0.0.0.0', port=port)

if __name__ == '__main__':
    main()
