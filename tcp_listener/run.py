from tcp_listener import run
import sys, imp

try:
    configs_filepath = sys.argv[1]
except:
    print("configs argument is required")
    sys.exit(1)

configs = imp.load_source(configs_filepath, configs_filepath)

if __name__ == '__main__':
    run(configs)


