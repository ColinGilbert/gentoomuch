import re

class kernel_sources_name_converter:
    def __init__(self):
        self.name = ''
        self.version = ''
        self.release = ''
        self.good = False

    def ingest_canonical_name(self, name: str):
        elems = name.split('-')
        if len(elems) < 3 or elems[0] != 'linux':
            self.good = False
            return
        self.version = elems[1]
        self.name = elems[2]
        if len(elems) > 3:
            if elems[3].startswith('r'):
                tag = elems[3]
                self.release = tag[1:]
        self.good = True

    def ingest_package_name(self, name: str):
        elems = name.split('-')
        if len(elems) < 3:
            self.good = False
            return
        self.name = elems[0]
        self.version = elems[2]
        if len(elems) > 3:
            if elems[3].startswith('r'):
                tag = elems[3]
                self.release = tag[1:]
        self.good = True

    def get_canonical_name(self): # linux-6.12.4-gentoo-r1
        return 'linux-' + self.version + '-' + self.name + (('-r' + self.release) if self.release != '' else '')

    def get_package_name(self): # gentoo-sources-6.12.4-r1
        return self.name + '-sources-' + self.version + (('-r' + self.release) if self.release != '' else '')


def test_kernel_sources_name_converter():
    test = kernel_sources_name_converter()
    canonical_name = 'linux-6.12.4-gentoo-r1'
    package_name = 'gentoo-sources-6.12.4-r1'
    test.ingest_canonical_name(canonical_name)
    if canonical_name == test.get_canonical_name():
        print('SUCCESS - Canonical name')
    else:
        print('FAILURE - Canonical name: ' + test.get_canonical_name())
    if package_name == test.get_package_name():
        print("SUCCESS - Package name")
    else:
        print('FAILURE - Package name')
    test.ingest_package_name(package_name)
    if package_name == test.get_package_name():
        print('SUCCESS - Package name 2')
    else:
        print('FAILURE - Package name 2')
    if canonical_name == test.get_canonical_name():
        print('SUCCESS - Canonical name 2')
    else:
        print('FAILURE - Canonical name 2')