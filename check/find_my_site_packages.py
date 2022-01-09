import site


def find_my_site_packages():
    # below should return
    # [
    #   ' python /root/.cache/activestate/868be8dc/lib/python2.7/site-packages/pipdeptree.py > /root/django/treefreeze.txt',
    #   '/root/.cache/activestate/868be8dc/lib/site-python'
    # ]
    pkgs_dir = site.getsitepackages()[0]
    # pkgs_dir = '/root/.cache/activestate/868be8dc/lib/python2.7/site-packages'
    print('I should be something similar to /root/.cache/activestate/868be8dc/lib/python2.7/site-packages')
    print(pkgs_dir)
    return pkgs_dir
