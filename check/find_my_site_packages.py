import site


def find_my_site_packages():
    """
    Static function to find your site package directory.
    :return: directory location of this python environment's site packages
    """
    pkgs_dir = site.getsitepackages()[0]
    # [
    #   ' /root/.cache/activestate/868be8dc/lib/python2.7/site-packages/',
    #   '/root/.cache/activestate/868be8dc/lib/site-python'
    # ]
    # pkgs_dir = '/root/.cache/activestate/868be8dc/lib/python2.7/site-packages'
    print('I should be something similar to /root/.cache/activestate/868be8dc/lib/python2.7/site-packages')
    print(pkgs_dir)
    return pkgs_dir
