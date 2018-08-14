import getopt
import os
import sys


class Arguments(list):

    def __init__(self, config={}, usage='', description='', example=''):
        self.config = config
        if not self.config.has_key('h'):
            self.config['h'] = ('help', '', 'This page')
        self.appname = os.path.basename(sys.argv[0])
        self.usage = usage % self.appname
        self.description = description
        self.example = example % self.appname
        self.options = {}
        self.maxlength = 0

        shortopts = []
        longopts = []
        for k in self.config.keys():
            option, value, desc = self.config[k]
            shortopts.append(k)
            if value:
                shortopts.append(':')
                longopts.append(option + '=')
            else:
                longopts.append(option)
            n = len(option) + len(value)
            if n > self.maxlength:
                self.maxlength = n

        parsed, leftover = getopt.getopt(sys.argv[1:], ''.join(shortopts),
                                         longopts)
        for option, value in parsed:
            if option.startswith('--'):
                option = option[2:]
            else:
                option = self.config[option[1:]][0]
            self.options[option] = value
        self.extend(leftover)

    def help(self):
        print self.usage
        print self.description
        print self.example
        seq = self.config.keys()
        seq.sort()
        for k in seq:
            option, value, desc = self.config[k]
            n = len(option) + len(value)
            if value:
                print '  -%s, --%s=%s%s%s' % (k, option, value,
                                              (self.maxlength - n + 1) * ' ',
                                              desc)
            else:
                print '  -%s, --%s%s%s' % (k, option,
                                           (self.maxlength - n + 2) * ' ',
                                           desc)
