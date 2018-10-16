import sys


def validateFileName(number):
    correctFileNumbers = ['10', '20', '50', '100', '200', '500', '1000']
    return number in correctFileNumbers


def validateArguments(args):
    return len(args) >= 3


def validateInstanceNo(instanceNumber):
    print([str(i) for i in list(range(1, 11))])
    return instanceNumber in [str(i) for i in list(range(1, 11))]


def validateParamH(h):
    return h in ['0.2', '0.4', '0.6', '0.8']


def main():
    print('RUN as main.py FILE_NUMBER K H')

    if validateArguments(sys.argv) and validateFileName(sys.argv[1]) and \
       validateInstanceNo(sys.argv[2]) and validateParamH(sys.argv[3]):
        print(sys.argv)


if __name__ == '__main__':
    main()
