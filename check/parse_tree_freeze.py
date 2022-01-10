import pandas as pd
import os
from .get_import_names import get_import_names
from .find_my_site_packages import find_my_site_packages


def find_name(r):
    """
    finds the package name without version number
    :params r: requirement row

    example:
    pkg                | symbloc (symbol location)
    _____________________________________________
    matplotlib~=3.4.3 | 10
    numpy>1.20        | 5
    pandas            | 0

    :returns cleaned name
        matplotlib
        numpy
        pandas
    """
    if r['symbloc'] == 0:
        # if no version return package
        # matplotlib
        return r['pkg']
    else:
        # if no version matplotlib~=3.4.3
        # return package name indexed at the symbol or just
        # matplotlib
        return r['pkg'][:r['symbloc']]


def find_symb(r):
    """
    finds the symbol index location within the package name
    :params r: requirement name with version

    examples:
    pkg
    __________________
    matplotlib~=3.4.3
    numpy>1.20
    pandas

    :returns symbloc (symbol location)
        10
        5
        0
    """
    symbs = ["==", ">", ">=", "<", "<=", "~=", "~", "@"]
    symb = [r.find(symb[0]) for symb in symbs if symb in r]
    if len(symb) > 0:
        # this finds requirements with versions
        # matplotlib~=3.4.3 finds "~=" at position 10
        # returns 10
        return symb[0]
    else:
        # this finds requirements with no versions
        # matplotlib
        return 0


def iter_packages(pkg_names):
    """
    :param pkg_names: a pd series with requirements and their dependencies

    amazon-dax-client==1.1.8
      antlr4-python2-runtime==4.7.2
      botocore==1.20.112
        jmespath==0.10.0
        python-dateutil==2.8.2
          six==1.16.0
        urllib3==1.26.4
      futures==3.3.0
      six==1.16.0
    amazon-dax-client is the requirements
    everything indented under it is the dependencies of the above req

    :return: a pd dataframe with the requirement and it's dependencies
    """
    site_pkg_directory = find_my_site_packages()
    import_names = get_import_names()
    req_dep = pd.DataFrame(columns=['pkg', 'dep'])
    req = ''
    for index, req_or_dep in pkg_names.iteritems():
        req_or_dep = req_or_dep.rstrip()
        if req_or_dep.startswith('  '):
            # then it's a dependency
            dep = req_or_dep
            # remove indents
            dep = dep.lstrip()
            try:
                dep = import_names.loc[dep]['import_name']
                l_req_dep = pd.DataFrame(data=[[req, dep]], columns=['pkg', 'dep'])
            except KeyError:
                print('Error Dependency ' + dep + ' of ' + req + 'not  found in ' + site_pkg_directory)
        else:
            # then it's a requirement
            req = req_or_dep
            try:
                req = import_names.loc[req]['import_name']
                l_req_dep = pd.DataFrame(data=[[req, req]], columns=['pkg', 'dep'])
            except KeyError:
                print('Error Requirement ' + req + ' not found in ' + site_pkg_directory)

        req_dep = req_dep.append(l_req_dep)

    # sets index for faster look ups
    req_dep.set_index('pkg', inplace=True)
    return req_dep


def parse_requirements(proj):
    """
    Reads the treefreeze.txt to create a pandas dataframe to check pylint results
    """
    with open(os.path.join(proj, 'requirements.txt'), 'r') as file:
        reqs = pd.Series([line for line in file])

    symb_loc = pd.DataFrame([reqs, reqs.apply(lambda r: find_symb(r))], index=['pkg', 'symbloc']).T
    # pkg_names series
    pkg_names = symb_loc.apply(lambda r: find_name(r), axis='columns')
    # series names become column titles
    pkg_names = pkg_names.rename('pkg')
    return pkg_names


def parse_tree_freeze(proj):
    """
    Reads the treefreeze.txt to create a pandas dataframe to check pylint results
    """
    reqs = parse_requirements(proj)
    with open(os.path.join(proj, 'treefreeze.txt'), 'r') as file:
        tree_file = pd.Series([line for line in file])

    tree_file = pd.Series(tree_file)
    # symbol location: dataframe
    symb_loc = pd.DataFrame([tree_file, tree_file.apply(lambda r: find_symb(r))], index=['pkg', 'symbloc']).T
    # pkg_names series
    pkg_names = symb_loc.apply(lambda r: find_name(r), axis='columns')
    pkg_names = pkg_names.rename('pkg')

    not_in_tree_file = reqs[~reqs.isin(pkg_names)]
    pkg_names = pkg_names.append(not_in_tree_file)
    req_dep = iter_packages(pkg_names)
    # creates the base for requirements.csv
    # starts as 0 and becomes 1 when we encounter the import later
    req_dep['used'] = 0
    return req_dep
