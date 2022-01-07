import pandas as pd
import os


def parse_requirements(proj):
    """
    Reads the requirements.txt to create a pandas dataframe to check pylint results
    """
    with open(os.path.join(proj, 'requirements.txt'), 'r') as file:
        reqs = pd.Series([line for line in file])
        reqs = reqs.str.replace('\n', "")

        def find_smb(r):
            """
            finds the package name without version number
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

        # runs the two functions above and adds column names
        # ... well index names that get transposed into column names
        # symbol location: dataframe
        symb_loc = pd.DataFrame([reqs, reqs.apply(lambda r: find_smb(r))], index=['pkg', 'symbloc']).T
        # pkg_names series
        pkg_names = symb_loc.apply(lambda r: find_name(r), axis='columns')
        # series names become column titles
        pkg_names = pkg_names.rename('pkg')
        pkg_names = pkg_names.to_frame()
        # creates the base for requirements.csv
        # starts as 0 and becomes 1 when we encounter the import later
        pkg_names['used'] = 0
        # sets index for faster look ups
        pkg_names.set_index('pkg', inplace=True)
        return pkg_names
