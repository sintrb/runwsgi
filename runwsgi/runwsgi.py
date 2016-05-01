import sys, os
from wsgiref.simple_server import make_server

def print_help():
    print 'Usage: python -m runwsgi -b [host:port] model:applicaon'
    print 'Report bugs to <sintrb@gmail.com>'

def main():
    import getopt
    opts, args = getopt.getopt(sys.argv[1:], "hb:")
    host = '0.0.0.0'
    port = 8080
    for opt, arg in opts:
        if opt == '-b':
            if ':' in arg:
                host, port = arg.split(':')
                port = int(port)
            else:
                port = int(arg)
        elif opt == '-h':
            print_help()
            exit()
    if len(args) == 0:
        print_help()
        exit(-1)
    app_path = args[0]
    modules, application = app_path.split(':')
    sys.path.insert(0, os.getcwd())
    module = __import__(modules)
    for m in modules.split('.')[1:]:
        module = getattr(module, m)

    application = getattr(module, application)
    httpd = make_server(host, port, application)
    print 'Serving HTTP on {host}:{port}...'.format(host=host, port=port)
    httpd.serve_forever()
    
if __name__ == '__main__':
    main()
